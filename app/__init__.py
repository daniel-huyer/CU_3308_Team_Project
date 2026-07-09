# app/__init__.py
from flask import Flask, request
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    
    app = Flask(__name__)#, root_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    from app.routes import main
    app.register_blueprint(main)

    from app.models import db
    db.init_app(app)
    
    return app