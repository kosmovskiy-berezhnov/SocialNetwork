from app import db


class Moderator(db.Model):
    mod_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    com_id = db.Column(db.Integer, db.ForeignKey('community.id', ondelete='CASCADE'), primary_key=True)
