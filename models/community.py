from safrs import SAFRSBase

from config import db

from models.moderator import Moderator
from sqlalchemy.dialects import postgresql

from models.post import Post

banned_users = db.Table('banned_users',
                        db.Column('community_id', db.Integer, db.ForeignKey('community.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))
subscribe_table = db.Table('subscribeUsers',
                           db.Column('community_id', db.Integer, db.ForeignKey('community.id'), primary_key=True),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))
mods = db.Table('mods',
                db.Column('community_id', db.Integer, db.ForeignKey('community.id'), primary_key=True),
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class Community(SAFRSBase, db.Model):
    __tablename__ = 'community'
    '''
        description: a community of SocialNetwork
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    # banned_users = db.Column(postgresql.ARRAY(db.String(30), dimensions=1), default=[])
    banned_users = db.relationship('User', secondary=banned_users, back_populates='banned_communities')
    posts = db.relationship(Post, cascade='all, delete', backref='community')
    subscribers = db.relationship('User', secondary=subscribe_table, back_populates='communities')
    mods = db.relationship('User', secondary=mods, back_populates='modded')
    # subscribe_user = db.relationship(User, secondary=subscribe_table, passive_deletes=True,
    #     #                                  backref=db.backref("user_subscribe", passive_deletes=True),
    #     #                                  primaryjoin=subscribe_table.c.com_id == id,
    #     #                                  secondaryjoin=subscribe_table.c.user_id == User.id
    #     #                                  )
    # moderators_users = db.relationship('User', secondary='moderator', passive_deletes=True,
    #                                    primaryjoin=Moderator.com_id == id,
    #                                    secondaryjoin=Moderator.mod_id == User.id,
    #                                    backref=db.backref("users_moderators", passive_deletes=True))
