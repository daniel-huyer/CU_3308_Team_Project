# app/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash
from app.models import User

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

        session['user_id'] = user.id
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')