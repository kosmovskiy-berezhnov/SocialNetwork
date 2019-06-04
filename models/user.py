from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from config import db
from safrs import SAFRSBase

from models.comment import Comment
from models.post import Post
from models.community import banned_users, subscribe_table, mods


class User(SAFRSBase, db.Model, UserMixin):
    __tablename__ = 'user'
    '''
        description: User description
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(256), nullable=False)
    notifications = db.Column(JSON, nullable=True, default ='[]')
    posts = db.relationship(Post, backref='author', cascade='all, delete')
    comments = db.relationship(Comment, backref='author', cascade='all, delete')
    evaluated_comments = db.relationship(Comment, backref='evaluated_by')
    evaluated_posts = db.relationship(Post, backref='evaluated_by')
    banned_communities = db.relationship('Community', secondary=banned_users, back_populates='banned_users')
    communities = db.relationship('Community', secondary=subscribe_table, back_populates='subscribers')
    modded = db.relationship('Community', secondary=mods, back_populates='mods')

    def get_username(self):
        return self.username

    def get_notifications(self):
        return self.notifications

    def get_rating(self):
        pass

    def change_rating(self):
        pass

    def subscribe(self, community):
        pass

    def checkPas(self, pas):
        return self.password == pas
