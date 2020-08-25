import os
import time

from shared_resources import db, ma
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_required
import users
from users import User
import post
from json_maker import is_logged_in_json


def create_app():
    # Init app
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SECRET KEY
    # app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SECRET_KEY'] = b'a4"\x1aga\xab\xde\xdd\x89\xae\x8eO\xfb\xa8<'

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_id)

    # Init db
    db.init_app(app)
    # Init ma
    ma.init_app(app)
    # register the blueprint (views of users)
    app.register_blueprint(users.bp)
    app.register_blueprint(post.bp)

    # test if the website is working
    @app.route('/time')
    def get_current_time():
        return jsonify({'time': time.time()})

    @app.route('/logged')
    @login_required
    def is_logged_in():
        return is_logged_in_json(login_status=True)

    return app
