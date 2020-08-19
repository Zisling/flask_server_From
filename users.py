from flask import Flask, request, jsonify , session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from app import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True)
    last_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    permissions = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, permissions, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.permissions = permissions
        self.password = password


# Product Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'permissions', 'password')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
