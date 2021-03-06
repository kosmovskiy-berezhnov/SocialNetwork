from safrs import SAFRSBase

from config import db
from models.moderator import Moderator
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
    banned_table = db.Table('banned_users', db.metadata,
                            db.Column('com_id', db.Integer, db.ForeignKey('community.id', ondelete='CASCADE'),
                                      primary_key=True),
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                                      primary_key=True))
    banned_users = db.relationship(User, secondary=banned_table, passive_deletes=True,
                                   backref=db.backref("banned_com", passive_deletes=True),
                                   primaryjoin=banned_table.c.com_id == id,
                                   secondaryjoin=banned_table.c.user_id == User.id)
    subscribe_table = db.Table('subscribeUsers', db.metadata,
                               db.Column('com_id', db.Integer, db.ForeignKey(id, ondelete='CASCADE'), primary_key=True),
                               db.Column('user_id', db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'),
                                         primary_key=True)
                               )

    subscribe_user = db.relationship(User, secondary=subscribe_table, passive_deletes=True,
                                     backref=db.backref("user_subscribe", passive_deletes=True),
                                     primaryjoin=subscribe_table.c.com_id == id,
                                     secondaryjoin=subscribe_table.c.user_id == User.id
                                     )
    moderators_users = db.relationship(User, secondary='moderator', passive_deletes=True,
                                       primaryjoin=Moderator.com_id == id,
                                       secondaryjoin=Moderator.mod_id == User.id,
                                       backref=db.backref("users_moderators", passive_deletes=True))
