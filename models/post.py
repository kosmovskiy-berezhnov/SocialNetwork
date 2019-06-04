from safrs import SAFRSBase

from config import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

from models.comment import Comment

class Post(SAFRSBase, db.Model):
    __tablename__ = 'post'
    '''
        description: Post
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    html_page = db.Column(db.Text)
    comments = db.relationship(Comment, backref='post', cascade='all, delete')
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # author = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'), nullable=False)
    # authorrel = db.relationship(User, lazy="joined", backref="posts")
    # post_comments = db.relationship(Comment, passive_deletes=True,
    #                                 backref=db.backref("comment_post", passive_deletes=True))
    # evaluatedusers = db.Column(db.Text, nullable=False, default='')
    # post_community = db.relationship(Community, passive_deletes=True,lazy="joined",
    #                                  backref=db.backref("community_posts", passive_deletes=True))

    def set_html_page(self, nhtml_page):
        self.html_page = nhtml_page

    def get_html_page(self):
        return self.html_page
