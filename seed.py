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

from app import create_app
from app.db import db
from app.models import User, Category
# TODO: import additional models as they are built
#from app.models import Category, Transaction, Budget

from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    # -------------------------------------------------------------------------
    # Clear existing data
    # -------------------------------------------------------------------------
    print("Clearing existing data...")
    # TODO: delete in reverse dependency order as models are added
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
    # TODO: add sample transaction data when Transaction model is built (Issue 2.2)
    # -------------------------------------------------------------------------
    expense_categories = [
        "Food",
        "Transportation",
        "Utilities",
        "Entertainment",
        "Healthcare",
        "Housing",
    ]

    income_categories = [
        "Paycheck",
        "Freelance",
        "Gift",
        "Other",
    ]

    for name in expense_categories:
        
        db.session.add(
            Category(
                name=name,
                type="expense",
                user_id=demo_user.id,
            )
        )

    for name in income_categories:
        db.session.add(
            Category(
                name=name,
                type="income",
                user_id=demo_user.id,
            )
        )    

    db.session.commit()

    # -------------------------------------------------------------------------
    # Seed Transactions
    # TODO: add sample transaction data when Transaction model is built (Issue 2.3)
    # -------------------------------------------------------------------------
    # Sample transactions:
    #
    #
    # for t in sample_transactions:
    #     transaction = Transaction(
    #         user_id=demo_user.id,
    #         # add more fields here...
    #     )
    #     db.session.add(transaction)
    # db.session.commit()

    # -------------------------------------------------------------------------
    # Seed Budgets
    # TODO: add sample budget data when Budget model is built (Issue 2.4)
    # -------------------------------------------------------------------------
    # Sample budgets:
    #
    #
    # for b in sample_budgets:
    #     budget = Budget(
    #         user_id=demo_user.id,
    #         # add more fields here...
    #     )
    #     db.session.add(budget)
    # db.session.commit()

    # TODO: add additional tables as needed

    print("\nSeeding complete.")
    print(f"Demo login -> username: demo  password: password123")