# app/routes.py
from datetime import date, datetime

from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models import Budget, Category, Transaction, User


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("home.html")


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")


@main.route("/budgets")
def budgets():
    return render_template("budgets.html")


@main.route("/admin/users")
@login_required
def db_test():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()
    return render_template("admin/users.html", users=users)


# ========================== Transaction Routes ========================

@main.route("/api/transactions", methods=["GET"])
@login_required
def get_transactions():
    query = Transaction.query.filter_by(
        user_id=current_user.id
    )

    keyword = request.args.get("keyword", "").strip()
    transaction_type = request.args.get("type", "").strip()
    category_id = request.args.get("category_id", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()

    if keyword:
        query = query.filter(
            Transaction.note.ilike(f"%{keyword}%")
        )

    if transaction_type:
        if transaction_type not in ("income", "expense"):
            return jsonify({
                "status": "error",
                "message": (
                    "Transaction type must be income or expense."
                )
            }), 400

        query = query.filter(
            Transaction.type == transaction_type
        )

    if category_id:
        try:
            category_id_value = int(category_id)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Category ID must be a number."
            }), 400

        query = query.filter(
            Transaction.category_id == category_id_value
        )

    try:
        if start_date:
            parsed_start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            query = query.filter(
                Transaction.date >= parsed_start_date
            )

        if end_date:
            parsed_end_date = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

            query = query.filter(
                Transaction.date <= parsed_end_date
            )

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Dates must use YYYY-MM-DD format."
        }), 400

    transactions = query.order_by(
        Transaction.date.desc(),
        Transaction.id.desc()
    ).all()

    return jsonify({
        "status": "success",
        "data": [
            {
                "id": transaction.id,
                "date": transaction.date.isoformat(),
                "description": transaction.note or "",
                "category_id": transaction.category_id,
                "category_name": (
                    transaction.category.name
                    if transaction.category
                    else "Unknown"
                ),
                "amount": float(transaction.amount),
                "type": transaction.type
            }
            for transaction in transactions
        ]
    })


@main.route("/api/transactions", methods=["POST"])
@login_required
def create_transaction():
    data = request.get_json() or {}

    transaction_date = date.today()

    if data.get("date"):
        try:
            transaction_date = datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Date must use YYYY-MM-DD format."
            }), 400

    transaction = Transaction(
        user_id=current_user.id,
        category_id=data.get("category_id"),
        amount=data.get("amount"),
        type=data.get("type"),
        date=transaction_date,
        note=data.get("note")
    )

    try:
        db.session.add(transaction)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": (
                "Unable to create transaction. "
                "Check the entered values."
            )
        }), 400

    return jsonify({
        "status": "success",
        "message": "Transaction created",
        "id": transaction.id
    }), 201


@main.route("/api/transactions/<int:tid>", methods=["PUT"])
@login_required
def update_transaction(tid):
    transaction = Transaction.query.filter_by(
        id=tid,
        user_id=current_user.id
    ).first()

    if not transaction:
        return jsonify({
            "status": "error",
            "message": "Transaction not found"
        }), 404

    data = request.get_json() or {}

    if "amount" in data:
        transaction.amount = data["amount"]

    if "note" in data:
        transaction.note = data["note"]

    if "type" in data:
        transaction.type = data["type"]

    if "category_id" in data:
        transaction.category_id = data["category_id"]

    if "date" in data:
        try:
            transaction.date = datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Date must use YYYY-MM-DD format."
            }), 400

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": (
                "Unable to update transaction. "
                "Check the entered values."
            )
        }), 400

    return jsonify({
        "status": "success",
        "message": "Transaction updated"
    })


@main.route("/api/transactions/<int:tid>", methods=["DELETE"])
@login_required
def delete_transaction(tid):
    transaction = Transaction.query.filter_by(
        id=tid,
        user_id=current_user.id
    ).first()

    if not transaction:
        return jsonify({
            "status": "error",
            "message": "Transaction not found"
        }), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Transaction deleted"
    })


# ========================== Category Routes ===========================

@main.route("/api/categories", methods=["GET"])
@login_required
def get_categories():
    categories = Category.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "status": "success",
        "data": [
            {
                "id": category.id,
                "name": category.name,
                "type": category.type
            }
            for category in categories
        ]
    })


@main.route("/api/categories", methods=["POST"])
@login_required
def create_category():
    data = request.get_json() or {}

    category = Category(
        name=data["name"],
        type=data["type"],
        user_id=current_user.id
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Category created",
        "id": category.id
    })


# =========================== Budget Routes ============================

@main.route("/api/budgets", methods=["GET"])
@login_required
def get_budgets():
    budgets = Budget.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "status": "success",
        "data": [
            {
                "id": budget.id,
                "category_id": budget.category_id,
                "month": budget.month,
                "limit_amount": float(budget.limit_amount)
            }
            for budget in budgets
        ]
    })


@main.route("/api/budgets", methods=["POST"])
@login_required
def create_budget():
    data = request.get_json() or {}

    budget = Budget(
        user_id=current_user.id,
        category_id=data["category_id"],
        month=data["month"],
        limit_amount=data["limit_amount"]
    )

    db.session.add(budget)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": (
                "Budget already exists for this month "
                "and category."
            )
        }), 409

    return jsonify({
        "status": "success",
        "message": "Budget created",
        "id": budget.id
    }), 201


@main.route("/api/budgets/<int:bid>", methods=["PUT"])
@login_required
def update_budget(bid):
    budget = Budget.query.filter_by(
        id=bid,
        user_id=current_user.id
    ).first()

    if not budget:
        return jsonify({
            "status": "error",
            "message": "Budget not found"
        }), 404

    data = request.get_json() or {}

    if "limit_amount" in data:
        budget.limit_amount = data["limit_amount"]

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Budget updated"
    })


# ========================= Dashboard Summary ==========================

@main.route("/api/dashboard", methods=["GET"])
@login_required
def dashboard_summary():
    user_id = current_user.id

    total_income = db.session.query(
        db.func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income"
    ).scalar() or 0

    total_expenses = db.session.query(
        db.func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense"
    ).scalar() or 0

    return jsonify({
        "status": "success",
        "data": {
            "balance": float(total_income - total_expenses),
            "income": float(total_income),
            "expenses": float(total_expenses)
        }
    })