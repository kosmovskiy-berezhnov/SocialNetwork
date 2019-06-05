from config import db
from safrs import SAFRSBase

class Administrator(SAFRSBase,db.Model):
    from models.user import User
    username = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'), primary_key=True)
    admin_users = db.relationship(User, lazy="joined",passive_deletes=True, backref=db.backref("admin_users",passive_deletes=True))
