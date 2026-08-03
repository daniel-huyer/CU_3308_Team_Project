from werkzeug.security import generate_password_hash

from app.db import db
from app.models import Category, User


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


def test_successful_registration(client, app):
    response = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure-password",
            "confirm_password": "secure-password",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with app.app_context():
        user = User.query.filter_by(username="newuser").first()

        assert user is not None
        assert user.email == "newuser@example.com"

        categories = Category.query.filter_by(user_id=user.id).all()

        assert len(categories) == 10


def test_duplicate_username_rejected(client, app):
    with app.app_context():
        create_test_user(
            username="existinguser",
            email="existing@example.com",
        )

    response = client.post(
        "/register",
        data={
            "username": "existinguser",
            "email": "different@example.com",
            "password": "secure-password",
            "confirm_password": "secure-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Username already taken" in response.data

    with app.app_context():
        users = User.query.filter_by(username="existinguser").all()

        assert len(users) == 1


def test_successful_login(client, app):
    with app.app_context():
        user = create_test_user()

        user_id = str(user.id)

    response = client.post(
        "/login",
        data={
            "username": "alex",
            "password": "secure-password",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session.get("_user_id") == user_id


def test_invalid_login(client, app):
    with app.app_context():
        create_test_user()

    response = client.post(
        "/login",
        data={
            "username": "alex",
            "password": "wrong-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_logout_clears_session(client, app):
    with app.app_context():
        create_test_user()

    client.post(
        "/login",
        data={
            "username": "alex",
            "password": "secure-password",
        },
    )

    with client.session_transaction() as session:
        assert "_user_id" in session

    response = client.get(
        "/logout",
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "_user_id" not in session