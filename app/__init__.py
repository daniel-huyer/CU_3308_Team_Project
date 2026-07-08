from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from .db import db

load_dotenv()

migrate = Migrate()

def create_app():
  app = Flask(__name__)

  app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
      "SQLALCHEMY_DATABASE_URI"
  )
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  db.init_app(app)

  migrate.init_app(app, db)

  return app