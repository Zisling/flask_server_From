from flask import Flask, request, jsonify, session, Blueprint
from shared_resources import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user , UserMixin, logout_user


class User(db.Model, UserMixin):
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
@login_required
def index():
    return jsonify({'user_state': 'You are logged in {}'.format(current_user.email)})


@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'user_state': 'fail to login {}'.format(email)})
    login_user(user, remember=remember)
    return {'user_state': 'Logged in as %s' % email}


@bp.route('/logout', methods=['PUT'])
@login_required
def logout():
    email = current_user.email
    logout_user()
    return jsonify({'user_state': 'You are logged out {}'.format(email)})


@bp.route('/signup', methods=['POST'])
def signup():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"user status": "all ready exist"})

    new_user = User(first_name, last_name, email, 'normal', password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return {'user_state': 'signup as %s now go and login' % session[email]}
