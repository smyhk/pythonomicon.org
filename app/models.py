from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    subtitle = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
