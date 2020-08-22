from flask import Flask, request, jsonify, Blueprint
from shared_resources import db, ma
from flask_login import login_user, login_required, current_user, UserMixin, logout_user


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    subject = db.Column(db.String(100))
    text = db.Column(db.String(1000))

    def __init__(self, post_id, author, subject, text):
        self.post_id = post_id
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
