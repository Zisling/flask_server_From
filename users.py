from flask import Flask, request, jsonify, session
from shared_resources import db, ma
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


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

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def index():
    username = request.json['username']
    if username in session:
        return jsonify({'user_state': 'Logged in as %s' % session[username]})
    return jsonify({'user_state': 'You are not logged in'})


@bp.route('/login/<username>', methods=['POST'])
def login(username):
    session[username] = username
    return {'user_state': 'Logged in as %s' % session[username]}


@bp.route('/logout', methods=['PUT'])
def logout():
    # remove the username from the session if it's there
    username = request.json['username']
    session.pop(username, None)
    return jsonify({'user_state': 'You are logged out {}'.format(username)})
