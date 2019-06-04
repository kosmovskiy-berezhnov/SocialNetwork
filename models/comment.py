from safrs import SAFRSBase
from config import db


class Comment(SAFRSBase, db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'), nullable=False)
    # postid = db.Column(db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    # evaluatedusers = db.Column(db.Text, nullable=False, default='')
