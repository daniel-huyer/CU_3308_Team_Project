from datetime import date
from decimal import Decimal

import pytest
from werkzeug.security import generate_password_hash

from app.db import db
from app.models import Category, Transaction, User


def create_test_user(
    username="alex",
    email="alex@example.com",
    password="secure-password",
):
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )

    db.session.add(user)
    db.session.commit()

    return user


def create_test_category(user, name="Food", category_type="expense"):
    category = Category(
        name=name,
        type=category_type,
        user_id=user.id,
    )

    db.session.add(category)
    db.session.commit()

    return category


def login_test_user(client, username="alex", password="secure-password"):
    return client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False,
    )


def test_add_transaction(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)
        category_id = category.id

    login_test_user(client)

    response = client.post(
        "/api/transactions",
        json={
            "category_id": category_id,
            "amount": 42.50,
            "type": "expense",
            "date": "2026-08-01",
            "note": "Groceries",
        },
    )

    assert response.status_code == 201

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert response_data["message"] == "Transaction created"

    with app.app_context():
        transaction = db.session.get(
            Transaction,
            response_data["id"],
        )

        assert transaction is not None
        assert transaction.category_id == category_id
        assert transaction.amount == Decimal("42.50")
        assert transaction.type == "expense"
        assert transaction.date == date(2026, 8, 1)
        assert transaction.note == "Groceries"


def test_edit_transaction(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        transaction = Transaction(
            user_id=user.id,
            category_id=category.id,
            amount=Decimal("25.00"),
            type="expense",
            date=date(2026, 8, 1),
            note="Original note",
        )

        db.session.add(transaction)
        db.session.commit()

        transaction_id = transaction.id

    login_test_user(client)

    response = client.put(
        f"/api/transactions/{transaction_id}",
        json={
            "amount": 35.75,
            "date": "2026-08-02",
            "note": "Updated note",
        },
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert response_data["message"] == "Transaction updated"

    with app.app_context():
        updated_transaction = db.session.get(
            Transaction,
            transaction_id,
        )

        assert updated_transaction.amount == Decimal("35.75")
        assert updated_transaction.date == date(2026, 8, 2)
        assert updated_transaction.note == "Updated note"


def test_delete_transaction(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        transaction = Transaction(
            user_id=user.id,
            category_id=category.id,
            amount=Decimal("15.00"),
            type="expense",
            date=date(2026, 8, 1),
            note="Delete this transaction",
        )

        db.session.add(transaction)
        db.session.commit()

        transaction_id = transaction.id

    login_test_user(client)

    response = client.delete(
        f"/api/transactions/{transaction_id}"
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert response_data["message"] == "Transaction deleted"

    with app.app_context():
        deleted_transaction = db.session.get(
            Transaction,
            transaction_id,
        )

        assert deleted_transaction is None


def test_list_transactions(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        first_transaction = Transaction(
            user_id=user.id,
            category_id=category.id,
            amount=Decimal("20.00"),
            type="expense",
            date=date(2026, 8, 1),
            note="First transaction",
        )

        second_transaction = Transaction(
            user_id=user.id,
            category_id=category.id,
            amount=Decimal("30.00"),
            type="expense",
            date=date(2026, 8, 2),
            note="Second transaction",
        )

        db.session.add_all(
            [
                first_transaction,
                second_transaction,
            ]
        )
        db.session.commit()

    login_test_user(client)

    response = client.get("/api/transactions")

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert len(response_data["data"]) == 2

    descriptions = [
        transaction["description"]
        for transaction in response_data["data"]
    ]

    assert "First transaction" in descriptions
    assert "Second transaction" in descriptions


@pytest.mark.parametrize(
    "method,url",
    [
        ("get", "/api/transactions"),
        ("post", "/api/transactions"),
        ("put", "/api/transactions/1"),
        ("delete", "/api/transactions/1"),
    ],
)
def test_unauthorized_access_redirects(client, method, url):
    request_method = getattr(client, method)

    if method in {"post", "put"}:
        response = request_method(
            url,
            json={},
            follow_redirects=False,
        )
    else:
        response = request_method(
            url,
            follow_redirects=False,
        )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]