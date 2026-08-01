from decimal import Decimal

from werkzeug.security import generate_password_hash

from app.db import db
from app.models import Budget, Category, User


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


def create_test_category(
    user,
    name="Food",
    category_type="expense",
):
    category = Category(
        name=name,
        type=category_type,
        user_id=user.id,
    )

    db.session.add(category)
    db.session.commit()

    return category


def login_test_user(
    client,
    username="alex",
    password="secure-password",
):
    return client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=False,
    )


def test_set_budget(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)
        category_id = category.id

    login_test_user(client)

    response = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "month": "2026-08",
            "limit_amount": 500.00,
        },
    )

    assert response.status_code == 201

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert response_data["message"] == "Budget created"

    with app.app_context():
        budget = db.session.get(
            Budget,
            response_data["id"],
        )

        assert budget is not None
        assert budget.category_id == category_id
        assert budget.month == "2026-08"
        assert budget.limit_amount == Decimal("500.00")


def test_update_budget(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        budget = Budget(
            user_id=user.id,
            category_id=category.id,
            month="2026-08",
            limit_amount=Decimal("500.00"),
        )

        db.session.add(budget)
        db.session.commit()

        budget_id = budget.id

    login_test_user(client)

    response = client.put(
        f"/api/budgets/{budget_id}",
        json={
            "limit_amount": 650.00,
        },
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert response_data["message"] == "Budget updated"

    with app.app_context():
        updated_budget = db.session.get(
            Budget,
            budget_id,
        )

        assert updated_budget.limit_amount == Decimal("650.00")


def test_duplicate_budget_returns_error(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        user_id = user.id
        category_id = category.id

        budget = Budget(
            user_id=user_id,
            category_id=category_id,
            month="2026-08",
            limit_amount=Decimal("500.00"),
        )

        db.session.add(budget)
        db.session.commit()

    login_test_user(client)

    response = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "month": "2026-08",
            "limit_amount": 600.00,
        },
    )

    assert response.status_code == 409

    response_data = response.get_json()

    assert response_data["status"] == "error"
    assert (
        response_data["message"]
        == "Budget already exists for this month and category."
    )

    with app.app_context():
        budgets = Budget.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            month="2026-08",
        ).all()

        assert len(budgets) == 1


def test_list_budgets(client, app):
    with app.app_context():
        user = create_test_user()
        category = create_test_category(user)

        budget = Budget(
            user_id=user.id,
            category_id=category.id,
            month="2026-08",
            limit_amount=Decimal("500.00"),
        )

        db.session.add(budget)
        db.session.commit()

    login_test_user(client)

    response = client.get("/api/budgets")

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["status"] == "success"
    assert len(response_data["data"]) == 1
    assert response_data["data"][0]["month"] == "2026-08"
    assert response_data["data"][0]["limit_amount"] == 500.00


def test_unauthorized_budget_access_redirects(client):
    response = client.get(
        "/api/budgets",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]