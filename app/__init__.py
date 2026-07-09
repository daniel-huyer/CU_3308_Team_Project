# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from app.db import db

migrate = Migrate()

def create_app():
    load_dotenv()
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import main
    app.register_blueprint(main)

    
    return app
