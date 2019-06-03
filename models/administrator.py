from config import db


class Administrator(db.Model):
    from models.user import User
    username = db.Column(db.ForeignKey(User.username), primary_key=True)
    admin_users = db.relationship(User, lazy="joined", backref=" admin_users", cascade='all,delete')
