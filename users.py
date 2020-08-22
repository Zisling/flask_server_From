from flask import Flask, request, jsonify, Blueprint
from shared_resources import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, UserMixin, logout_user
from json_maker import login_json, logout_json, signup_json


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


# USER Schema
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
    if current_user.is_authenticated:
        return jsonify({'user_state': 'You are logged in {}'.format(current_user.email)})


@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return login_json(login_status=False, first_name='user not found', last_name='user not found', email=email,
                          confirm=False)
    login_user(user, remember=remember)
    return login_json(login_status=True, first_name=user.first_name, last_name=user.last_name, email=user.email)


@bp.route('/logout', methods=['PUT'])
@login_required
def logout():
    email = current_user.email
    logout_user()
    return logout_json(login_status=False, email=email)


@bp.route('/signup', methods=['POST'])
def signup():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return signup_json(login_status=False, first_name=first_name, last_name=last_name, email=email)

    new_user = User(first_name, last_name, email, 'normal', password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return signup_json(login_status=False, first_name=first_name, last_name=last_name, email=email)
