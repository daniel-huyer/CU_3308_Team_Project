from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models import Budget, Category, Transaction, User


def test_user_password_hashing(app):
    user = User(
        username="alex",
        email="alex@example.com",
    )

    user.set_password("secure-password")

    assert user.password_hash != "secure-password"
    assert user.check_password("secure-password") is True
    assert user.check_password("wrong-password") is False


def test_duplicate_username_raises_error(app):
    user1 = User(
        username="alex",
        email="alex1@example.com",
    )
    user1.set_password("password1")

    user2 = User(
        username="alex",
        email="alex2@example.com",
    )
    user2.set_password("password2")

    db.session.add(user1)
    db.session.commit()

    db.session.add(user2)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()


def test_transaction_links_to_user_and_category(app):
    user = User(
        username="alex",
        email="alex@example.com",
    )
    user.set_password("password")

    db.session.add(user)
    db.session.commit()

    category = Category(
        name="Groceries",
        type="expense",
        user=user,
    )

    db.session.add(category)
    db.session.commit()

    transaction = Transaction(
        user=user,
        category=category,
        amount=Decimal("45.75"),
        type="expense",
        date=date.today(),
        note="Weekly groceries",
    )

    db.session.add(transaction)
    db.session.commit()

    saved_transaction = db.session.get(
        Transaction,
        transaction.id,
    )

    assert saved_transaction.user == user
    assert saved_transaction.category == category
    assert saved_transaction in user.transactions
    assert saved_transaction in category.transactions


def test_budget_unique_constraint(app):
    user = User(
        username="alex",
        email="alex@example.com",
    )
    user.set_password("password")

    db.session.add(user)
    db.session.commit()

    category = Category(
        name="Food",
        type="expense",
        user=user,
    )

    db.session.add(category)
    db.session.commit()

    budget1 = Budget(
        user_id=user.id,
        category_id=category.id,
        month="2026-07",
        limit_amount=Decimal("500.00"),
    )

    db.session.add(budget1)
    db.session.commit()

    budget2 = Budget(
        user_id=user.id,
        category_id=category.id,
        month="2026-07",
        limit_amount=Decimal("600.00"),
    )

    db.session.add(budget2)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()