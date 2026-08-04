# app/routes.py
from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    jsonify,
)
from flask_login import (
    login_required,
    current_user,
)
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models import (
    User,
    Transaction,
    Category,
    Budget,
)
from datetime import date, datetime

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("home.html")


@main.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html"
    )


@main.route("/transactions")
@login_required
def transactions():
    return render_template(
        "transactions.html"
    )


@main.route("/budgets")
@login_required
def budgets():
    return render_template(
        "budgets.html"
    )


@main.route("/admin/users")
@login_required
def db_test():
    if not current_user.is_admin:
        abort(403)

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )


# ========================== Transaction Routes ========================

@main.route(
    "/api/transactions",
    methods=["GET"]
)
@login_required
def get_transactions():
    query = Transaction.query.filter_by(
        user_id=current_user.id
    )

    keyword = request.args.get(
        "keyword"
    )

    type_filter = request.args.get(
        "type"
    )

    category_id = request.args.get(
        "category_id"
    )

    start_date = request.args.get(
        "start_date"
    )

    end_date = request.args.get(
        "end_date"
    )

    if keyword:
        query = query.filter(
            Transaction.note.ilike(
                f"%{keyword}%"
            )
        )

    if type_filter:
        query = query.filter(
            Transaction.type ==
            type_filter
        )

    if category_id:
        query = query.filter(
            Transaction.category_id ==
            int(category_id)
        )

    if start_date:
        query = query.filter(
            Transaction.date >=
            datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()
        )

    if end_date:
        query = query.filter(
            Transaction.date <=
            datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()
        )

    transactions = query.order_by(
        Transaction.date.desc()
    ).all()

    return jsonify({
        "status": "success",

        "data": [{
            "id":
                transaction.id,

            "date":
                transaction.date.isoformat(),

            "description":
                transaction.note,

            "category_id":
                transaction.category_id,

            "category_name": (
                transaction.category.name
                if transaction.category
                else None
            ),

            "amount":
                float(
                    transaction.amount
                ),

            "type":
                transaction.type

        } for transaction in transactions]
    })


@main.route(
    "/api/transactions",
    methods=["POST"]
)
@login_required
def create_transaction():
    data = request.get_json() or {}

    transaction_date = date.today()

    if data.get("date"):
        transaction_date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

    transaction = Transaction(
        user_id=current_user.id,
        category_id=data.get(
            "category_id"
        ),
        amount=data.get(
            "amount"
        ),
        type=data.get(
            "type"
        ),
        date=transaction_date,
        note=data.get(
            "note"
        )
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Transaction created",
        "id": transaction.id
    }), 201


@main.route(
    "/api/transactions/<int:tid>",
    methods=["PUT"]
)
@login_required
def update_transaction(tid):
    transaction = Transaction.query.filter_by(
        id=tid,
        user_id=current_user.id
    ).first()

    if not transaction:
        return jsonify({
            "status": "error",
            "message":
                "Transaction not found"
        }), 404

    data = request.get_json() or {}

    if "amount" in data:
        transaction.amount = (
            data["amount"]
        )

    if "note" in data:
        transaction.note = (
            data["note"]
        )

    if "type" in data:
        transaction.type = (
            data["type"]
        )

    if "date" in data:
        transaction.date = (
            datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date()
        )

    if "category_id" in data:
        transaction.category_id = (
            data["category_id"]
        )

    db.session.commit()

    return jsonify({
        "status": "success",
        "message":
            "Transaction updated"
    })


@main.route(
    "/api/transactions/<int:tid>",
    methods=["DELETE"]
)
@login_required
def delete_transaction(tid):
    transaction = Transaction.query.filter_by(
        id=tid,
        user_id=current_user.id
    ).first()

    if transaction:
        db.session.delete(
            transaction
        )

        db.session.commit()

        return jsonify({
            "status": "success",
            "message":
                "Transaction deleted"
        })

    return jsonify({
        "status": "error",
        "message":
            "Transaction not found"
    }), 404


# ========================== Category Routes ===========================

@main.route(
    "/api/categories",
    methods=["GET"]
)
@login_required
def get_categories():
    categories = Category.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Category.name.asc()
    ).all()

    return jsonify({
        "status": "success",

        "data": [{
            "id":
                category.id,

            "name":
                category.name,

            "type":
                category.type

        } for category in categories]
    })


@main.route(
    "/api/categories",
    methods=["POST"]
)
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

@main.route(
    "/api/budgets",
    methods=["GET"]
)
@login_required
def get_budgets():
    budgets = Budget.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Budget.month.desc(),
        Budget.id.desc()
    ).all()

    budget_data = []

    for budget in budgets:
        month_start = datetime.strptime(
            budget.month,
            "%Y-%m"
        ).date()

        if month_start.month == 12:
            next_month = date(
                month_start.year + 1,
                1,
                1
            )

        else:
            next_month = date(
                month_start.year,
                month_start.month + 1,
                1
            )

        spent_amount = db.session.query(
            db.func.sum(
                Transaction.amount
            )
        ).filter(
            Transaction.user_id ==
            current_user.id,

            Transaction.category_id ==
            budget.category_id,

            Transaction.type ==
            "expense",

            Transaction.date >=
            month_start,

            Transaction.date <
            next_month
        ).scalar() or 0

        remaining_amount = (
            budget.limit_amount -
            spent_amount
        )

        budget_data.append({
            "id":
                budget.id,

            "category_id":
                budget.category_id,

            "category_name": (
                budget.category.name
                if budget.category
                else None
            ),

            "month":
                budget.month,

            "limit_amount":
                float(
                    budget.limit_amount
                ),

            "spent_amount":
                float(
                    spent_amount
                ),

            "remaining_amount":
                float(
                    remaining_amount
                )
        })

    return jsonify({
        "status": "success",
        "data": budget_data
    })


@main.route(
    "/api/budgets",
    methods=["POST"]
)
@login_required
def create_budget():
    data = request.get_json() or {}

    category_id = data.get(
        "category_id"
    )

    month = data.get(
        "month"
    )

    limit_amount = data.get(
        "limit_amount"
    )

    if (
        category_id is None
        or not month
        or limit_amount is None
    ):
        return jsonify({
            "status": "error",
            "message": (
                "Category, month, and budget "
                "limit are required."
            )
        }), 400

    category = Category.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first()

    if not category:
        return jsonify({
            "status": "error",
            "message":
                "Category not found"
        }), 404

    try:
        limit_amount = float(
            limit_amount
        )

    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": (
                "Budget limit must "
                "be a number."
            )
        }), 400

    if limit_amount < 0:
        return jsonify({
            "status": "error",
            "message": (
                "Budget limit cannot "
                "be negative."
            )
        }), 400

    budget = Budget(
        user_id=current_user.id,
        category_id=category_id,
        month=month,
        limit_amount=limit_amount
    )

    db.session.add(budget)

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": (
                "Budget already exists for this "
                "month and category."
            )
        }), 409

    except ValueError as error:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    return jsonify({
        "status": "success",
        "message":
            "Budget created",
        "id":
            budget.id
    }), 201


@main.route(
    "/api/budgets/<int:bid>",
    methods=["PUT"]
)
@login_required
def update_budget(bid):
    budget = Budget.query.filter_by(
        id=bid,
        user_id=current_user.id
    ).first()

    if not budget:
        return jsonify({
            "status": "error",
            "message":
                "Budget not found"
        }), 404

    data = request.get_json() or {}

    if "limit_amount" not in data:
        return jsonify({
            "status": "error",
            "message":
                "Budget limit is required."
        }), 400

    try:
        limit_amount = float(
            data["limit_amount"]
        )

    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": (
                "Budget limit must "
                "be a number."
            )
        }), 400

    if limit_amount < 0:
        return jsonify({
            "status": "error",
            "message": (
                "Budget limit cannot "
                "be negative."
            )
        }), 400

    budget.limit_amount = (
        limit_amount
    )

    db.session.commit()

    return jsonify({
        "status": "success",
        "message":
            "Budget updated"
    })


# ======================== Dashboard Summary ===========================

@main.route(
    "/api/dashboard",
    methods=["GET"]
)
@login_required
def dashboard_summary():
    user_id = current_user.id

    total_income = db.session.query(
        db.func.sum(
            Transaction.amount
        )
    ).filter(
        Transaction.user_id ==
        user_id,

        Transaction.type ==
        "income"
    ).scalar() or 0

    total_expenses = db.session.query(
        db.func.sum(
            Transaction.amount
        )
    ).filter(
        Transaction.user_id ==
        user_id,

        Transaction.type ==
        "expense"
    ).scalar() or 0

    return jsonify({
        "status": "success",

        "data": {
            "balance": float(
                total_income -
                total_expenses
            ),

            "income": float(
                total_income
            ),

            "expenses": float(
                total_expenses
            )
        }
    })