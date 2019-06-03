from datetime import datetime

from safrs import SAFRSBase

from config import db
from models.moderator import Moderator
from models.post import Post
from models.user import User


class Community(SAFRSBase, db.Model):
    '''
        description: a community of SocialNetwork
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    banned_users = None
    subscribe_table = db.Table('subscribeUsers', db.metadata,
                               db.Column('com_id', db.Integer, db.ForeignKey(id), primary_key=True),
                               db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
                               )
    subscribe_user = db.relationship(User, secondary=subscribe_table, cascade='all,delete',
                                     backref=db.backref("user_subscribe", cascade='all,delete'),
                                     primaryjoin=subscribe_table.c.com_id == id,
                                     secondaryjoin=subscribe_table.c.user_id == User.id
                                     )
    # moderators_table = db.Table('moderators', db.metadata,
    #                             db.Column('com_id', db.Integer, db.ForeignKey(id), primary_key=True),
    #                             db.Column('mod_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
    #                             )
    moderators_users = db.relationship(User, secondary='moderator', cascade='all,delete',
                                       primaryjoin=Moderator.com_id == id,
                                       secondaryjoin=Moderator.mod_id == User.id,
                                       backref=db.backref("users_moderators", cascade='all,delete'))
    post_table = db.Table('communityPosts', db.metadata,
                          db.Column('com_id', db.Integer, db.ForeignKey(id), primary_key=True),
                          db.Column('post_id', db.Integer, db.ForeignKey(Post.id), primary_key=True)
                          )
    community_posts = db.relationship(Post, secondary=post_table, cascade='all,delete',
                                      backref=db.backref("posts_community", cascade='all,delete'))
    # def __init__(self):
    #
    #     self.posts
