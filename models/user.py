from models.community import Community
from app import db



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    _rating = 0
    _communities = None
    _notifications = None
    def get_username(self):
        return self.username

    def get_rating(self):
        pass

    def change_rating(self):
        pass

    def subscribe(self, community):
        pass
    def checkPas (self, pas):
        return self.password == pas