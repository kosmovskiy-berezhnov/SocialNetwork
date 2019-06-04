from safrs import SAFRSBase

from config import db


class Administrator(SAFRSBase, db.Model):
    from models.user import User
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("admin", uselist=False))
