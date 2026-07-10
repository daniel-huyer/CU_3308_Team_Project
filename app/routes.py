# app/routes.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

@main.route('/admin/users')
def db_test():
    from app.models import User
    users = User.query.all()
    rows = ''.join(f'<tr><td>{u.id}</td><td>{u.username}</td><td>{u.email}</td></tr>' for u in users)
    return f'''
        <table border="1">
            <tr><th>ID</th><th>Username</th><th>Email</th></tr>
            {rows}
        </table>
        <p>Row count: {len(users)}</p>
    '''
