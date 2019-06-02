from datetime import datetime

from app import db
from models.user import User


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    author = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'), nullable=False)
    postid = db.Column(db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    evaluatedusers = db.Column(db.Text, nullable=False, default='')
