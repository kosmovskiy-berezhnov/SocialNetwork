
from app import db
from sqlalchemy.dialects.postgresql import JSON

user_post = db.Table('user_post',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                     )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    _rating = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    _notifications = db.Column(JSON, nullable=True)
    posts = db.relationship("Post", secondary=user_post, backpopulates='users')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._rating = 0

    def get_username(self):
        return self.username

    def get_notifications(self):
        return self._notifications


    def get_rating(self):
        pass

    def change_rating(self):
        pass

    def subscribe(self, community):
        pass
    def checkPas (self, pas):
        return self.password == pas
db.create_all()