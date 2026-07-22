# app/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Category
from app.db import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return render_template('login.html', 
                                   error='Invalid username or password')

        login_user(user)
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', 
                                   error='Passwords do not match')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html',
                                   error='Username already taken')

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return render_template('register.html',
                                   error='Email already registered')

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.flush() # assigns new_user.id without committing

         # Seed default categories for new user
        default_expense_categories = [
            'Food', 'Transportation', 'Utilities', 
            'Entertainment', 'Healthcare', 'Housing'
        ]
        default_income_categories = [
            'Paycheck', 'Freelance', 
            'Gift', 'Other'
        ]

        for name in default_expense_categories:
            db.session.add(
                Category(name=name, type='expense', 
                         user_id=new_user.id))
        for name in default_income_categories:
            db.session.add(
                Category(name=name, type='income', 
                         user_id=new_user.id))

        db.session.commit()

        

        login_user(new_user)
        return redirect(url_for('main.dashboard'))
    return render_template('register.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))