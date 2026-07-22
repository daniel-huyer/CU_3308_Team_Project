# app/routes.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/admin/users')
def db_test():
    from app.models import User
    users = User.query.all()
    return render_template('admin/users.html', users=users)