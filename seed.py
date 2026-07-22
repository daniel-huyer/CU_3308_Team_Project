# seed.py
# Run this script to populate the database with demo data before a presentation
# or to reset your local database to a known state for testing.
#
# Usage:
#   source setup.cmds
#   python seed.py
#
# WARNING: This script clears all existing data before seeding.
# Do not run on a database with real user data.

from datetime import date
from app import create_app
from app.db import db
from app.models import User, Category, Transaction, Budget
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # -------------------------------------------------------------------------
    # Clear existing data (reverse dependency order)
    # -------------------------------------------------------------------------
    print("Clearing existing data...")
    Budget.query.delete()
    Transaction.query.delete()
    Category.query.delete()
    User.query.delete()
    db.session.commit()
    print("Done.")

    # -------------------------------------------------------------------------
    # Seed Users
    # -------------------------------------------------------------------------
    print("Seeding users...")
    demo_user = User(
        username='demo',
        email='demo@example.com',
        password_hash=generate_password_hash('password123')
    )
    db.session.add(demo_user)
    db.session.commit()
    print(f"Created user: {demo_user.username}")

    # -------------------------------------------------------------------------
    # Seed Categories
    # -------------------------------------------------------------------------
    print("Seeding categories...")
    expense_category_names = [
        "Food",
        "Transportation",
        "Utilities",
        "Entertainment",
        "Healthcare",
        "Housing",
    ]
    income_category_names = [
        "Paycheck",
        "Freelance",
        "Gift",
        "Other",
    ]

    expense_categories = {}
    for name in expense_category_names:
        cat = Category(name=name, type="expense", user_id=demo_user.id)
        db.session.add(cat)
        expense_categories[name] = cat

    income_categories = {}
    for name in income_category_names:
        cat = Category(name=name, type="income", user_id=demo_user.id)
        db.session.add(cat)
        income_categories[name] = cat

    db.session.commit()
    print(f"Created {len(expense_categories)} expense and {len(income_categories)} income categories.")

    # -------------------------------------------------------------------------
    # Seed Transactions (2 months of data for dashboard charts)
    # -------------------------------------------------------------------------
    print("Seeding transactions...")
    sample_transactions = [
        # June income
        {"amount": 2800.00, "type": "income",  "category": "Paycheck",       "date": date(2026, 6, 1),  "note": "June salary"},
        {"amount": 350.00,  "type": "income",  "category": "Freelance",      "date": date(2026, 6, 14), "note": "Web design project"},

        # June expenses
        {"amount": 1200.00, "type": "expense", "category": "Housing",        "date": date(2026, 6, 1),  "note": "June rent"},
        {"amount": 120.00,  "type": "expense", "category": "Utilities",      "date": date(2026, 6, 3),  "note": "Electric bill"},
        {"amount": 65.00,   "type": "expense", "category": "Utilities",      "date": date(2026, 6, 5),  "note": "Internet"},
        {"amount": 180.00,  "type": "expense", "category": "Food",           "date": date(2026, 6, 7),  "note": "Grocery run"},
        {"amount": 45.00,   "type": "expense", "category": "Transportation", "date": date(2026, 6, 9),  "note": "Gas"},
        {"amount": 90.00,   "type": "expense", "category": "Food",           "date": date(2026, 6, 12), "note": "Groceries"},
        {"amount": 55.00,   "type": "expense", "category": "Entertainment",  "date": date(2026, 6, 15), "note": "Dinner out"},
        {"amount": 30.00,   "type": "expense", "category": "Transportation", "date": date(2026, 6, 18), "note": "Bus pass"},
        {"amount": 75.00,   "type": "expense", "category": "Food",           "date": date(2026, 6, 20), "note": "Groceries"},
        {"amount": 40.00,   "type": "expense", "category": "Entertainment",  "date": date(2026, 6, 22), "note": "Streaming and apps"},
        {"amount": 110.00,  "type": "expense", "category": "Healthcare",     "date": date(2026, 6, 25), "note": "Doctor visit copay"},
        {"amount": 60.00,   "type": "expense", "category": "Food",           "date": date(2026, 6, 28), "note": "Groceries"},

        # July income
        {"amount": 2800.00, "type": "income",  "category": "Paycheck",       "date": date(2026, 7, 1),  "note": "July salary"},
        {"amount": 100.00,  "type": "income",  "category": "Gift",           "date": date(2026, 7, 4),  "note": "Birthday gift"},

        # July expenses
        {"amount": 1200.00, "type": "expense", "category": "Housing",        "date": date(2026, 7, 1),  "note": "July rent"},
        {"amount": 125.00,  "type": "expense", "category": "Utilities",      "date": date(2026, 7, 3),  "note": "Electric bill"},
        {"amount": 65.00,   "type": "expense", "category": "Utilities",      "date": date(2026, 7, 5),  "note": "Internet"},
        {"amount": 95.00,   "type": "expense", "category": "Food",           "date": date(2026, 7, 6),  "note": "Grocery run"},
        {"amount": 50.00,   "type": "expense", "category": "Transportation", "date": date(2026, 7, 8),  "note": "Gas"},
        {"amount": 85.00,   "type": "expense", "category": "Food",           "date": date(2026, 7, 10), "note": "Groceries"},
        {"amount": 75.00,   "type": "expense", "category": "Entertainment",  "date": date(2026, 7, 12), "note": "Concert tickets"},
        {"amount": 45.00,   "type": "expense", "category": "Food",           "date": date(2026, 7, 15), "note": "Groceries"},
        {"amount": 320.00,  "type": "expense", "category": "Healthcare",     "date": date(2026, 7, 16), "note": "Dental visit"},
        {"amount": 55.00,   "type": "expense", "category": "Transportation", "date": date(2026, 7, 18), "note": "Gas"},
        {"amount": 110.00,  "type": "expense", "category": "Food",           "date": date(2026, 7, 20), "note": "Groceries and household"},
    ]

    for t in sample_transactions:
        cat_lookup = income_categories if t["type"] == "income" else expense_categories
        transaction = Transaction(
            user_id=demo_user.id,
            category_id=cat_lookup[t["category"]].id,
            amount=t["amount"],
            type=t["type"],
            date=t["date"],
            note=t["note"],
        )
        db.session.add(transaction)

    db.session.commit()
    print(f"Created {len(sample_transactions)} transactions.")

    # -------------------------------------------------------------------------
    # Seed Budgets (July — current month)
    # Note: Healthcare is intentionally over budget for demo alert feature
    # -------------------------------------------------------------------------
    print("Seeding budgets...")
    sample_budgets = [
        {"category": "Food",           "limit_amount": 300.00},
        {"category": "Transportation", "limit_amount": 150.00},
        {"category": "Utilities",      "limit_amount": 200.00},
        {"category": "Entertainment",  "limit_amount": 60.00},
        {"category": "Healthcare",     "limit_amount": 100.00},
        {"category": "Housing",        "limit_amount": 1200.00},
    ]

    current_month = "2026-07"
    for b in sample_budgets:
        budget = Budget(
            user_id=demo_user.id,
            category_id=expense_categories[b["category"]].id,
            month=current_month,
            limit_amount=b["limit_amount"],
        )
        db.session.add(budget)

    db.session.commit()
    print(f"Created {len(sample_budgets)} budgets for {current_month}.")

    print("\nSeeding complete.")
    print("Demo login -> username: demo  password: password123")
    print("\nNote: Healthcare budget ($100) is intentionally exceeded by transactions ($320) to demonstrate budget alerts.")