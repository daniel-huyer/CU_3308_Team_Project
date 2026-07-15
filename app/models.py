# app/models.py
from datetime import date, datetime
import re

from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
   
    categories = db.relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    budgets = db.relationship(
        "Budget",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        self.check_password(self.password_hash, password)

