from sqlalchemy.dialects.postgresql import JSON

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(30), nullable=False)
    notifications = db.Column(JSON, nullable=True)

    # def __init__(self, username, password):
    #   self.username = username
    #   self.password = password
    #  self._rating = 0

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
