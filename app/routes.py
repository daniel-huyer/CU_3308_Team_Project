# app/routes.py
from flask import Blueprint, render_template, abort, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models import User, Transaction, Category, Budget
from datetime import date, datetime

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
    return render_template('admin/users.html', users=users)


# ========================== Transaction Routes ========================
@main.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    return jsonify({
        "status": "success",
        "data": [{
            "id": t.id,
            "date": t.date.isoformat(),
            "description": t.note,
            "category_id": t.category_id,
            "amount": float(t.amount),
            "type": t.type
        } for t in transactions]
    })

@main.route('/api/transactions', methods=['POST'])
@login_required
def create_transaction():
    data = request.get_json()

    transaction_date = date.today()

    if data.get("date"):
        transaction_date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

    transaction = Transaction(
        user_id=current_user.id,
        category_id=data.get('category_id'),
        amount=data.get('amount'),
        type=data.get('type'),
        date=transaction_date,
        note=data.get('note')
    )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Transaction created", "id": transaction.id}), 201

@main.route('/api/transactions/<int:tid>', methods=['PUT'])
@login_required
def update_transaction(tid):
   
    transaction = Transaction.query.filter_by(id=tid, user_id=current_user.id).first()
    if not transaction:
        return jsonify({"status": "error", "message": "Transaction not found"}), 404
    
    data = request.get_json()
    if 'amount' in data: transaction.amount = data['amount']
    if 'note' in data: transaction.note = data['note']
    if 'type' in data: transaction.type = data['type']
    if 'date' in data: 
        transaction.date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()
    if 'category_id' in data: transaction.category_id = data['category_id']
    
    db.session.commit()
    return jsonify({"status": "success", "message": "Transaction updated"})

@main.route('/api/transactions/<int:tid>', methods=['DELETE'])
@login_required
def delete_transaction(tid):
    
    transaction = Transaction.query.filter_by(id=tid, user_id=current_user.id).first()
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"status": "success", "message": "Transaction deleted"})
    return jsonify({"status": "error", "message": "Transaction not found"}), 404

# ====================== Category Routes ==========================
@main.route('/api/categories', methods=['GET'])
@login_required
def get_categories():

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        "status": "success",
        "data": [{"id": c.id, "name": c.name, "type": c.type} for c in categories]
    })

@main.route('/api/categories', methods=['POST'])
@login_required
def create_category():
    
    data = request.get_json()
    category = Category(
        name=data['name'],
        type=data['type'],
        user_id=current_user.id
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({"status": "success", "message": "Category created", "id": category.id})


# ======================== Budget Routes =========================
@main.route('/api/budgets', methods=['GET'])
@login_required
def get_budgets():
    
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        "status": "success",
        "data": [{
            "id": b.id,
            "category_id": b.category_id,
            "month": b.month,
            "limit_amount": float(b.limit_amount)
        } for b in budgets]
    })

@main.route('/api/budgets', methods=['POST'])
@login_required
def create_budget():
    
    data = request.get_json()
    budget = Budget(
        user_id=current_user.id,
        category_id=data['category_id'],
        month=data['month'],
        limit_amount=data['limit_amount']
    )
    db.session.add(budget)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Budget already exists for this month and category."
        }), 409


    return jsonify({"status": "success", "message": "Budget created", "id": budget.id}), 201

@main.route('/api/budgets/<int:bid>', methods=['PUT'])
@login_required
def update_budget(bid):
    
    budget = Budget.query.filter_by(id=bid, user_id=current_user.id).first()
    if not budget:
        return jsonify({"status": "error", "message": "Budget not found"}), 404
    data = request.get_json()
    if 'limit_amount' in data:
        budget.limit_amount = data['limit_amount']
    db.session.commit()
    return jsonify({"status": "success", "message": "Budget updated"})


# ======================== Dashboard Summary ========================
@main.route('/api/dashboard', methods=['GET'])
def dashboard_summary():

    user_id = current_user.id
    
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, Transaction.type == 'income'
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, Transaction.type == 'expense'
    ).scalar() or 0
    
    return jsonify({
        "status": "success",
        "data": {
            "balance": float(total_income - total_expenses),
            "income": float(total_income),
            "expenses": float(total_expenses)
        }
    })

