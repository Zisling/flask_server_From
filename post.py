from flask import Flask, request, jsonify, Blueprint
from shared_resources import db, ma
from flask_login import login_user, login_required, current_user, UserMixin, logout_user
from json_maker import post_json
from users import User
import json


class Post(db.Model):
    author = db.Column('author', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    subject = db.Column(db.String(100))
    text = db.Column(db.String(500))

    def __init__(self, author, subject, text):
        self.author = author
        self.subject = subject
        self.text = text


# USER Schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'subject', 'text')


# Init schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/', methods=['POST'])
@login_required
def post():
    author = current_user.id
    subject = request.json['subject']
    text = request.json['text']
    new_post = Post(author=author, subject=subject, text=text)
    db.session.add(new_post)
    db.session.commit()
    return post_json()


@bp.route('/', methods=['get'])
@login_required
def get_post():
    posts = Post.query.all()
    posts = jsonify(list(map(post_to_json, posts)))
    return posts


def post_to_json(post):
    user = User.query.filter_by(id=post.author).first()
    author = user.email
    return {
        'author': author,
        'subject': post.subject,
        'text': post.text
    }
