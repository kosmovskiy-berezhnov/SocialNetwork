from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

from app import db
from models.comment import Comment
from models.user import User
from models.community import Community

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    html_page = db.Column(db.Text)
    author = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'), nullable=False)
    authorrel = db.relationship(User, lazy="joined", backref=db.backref("authorrel", passive_deletes=True), passive_deletes=True)
    post_comments = db.relationship(Comment, passive_deletes=True,
                                    backref=db.backref("comment_post", passive_deletes=True))
    evaluatedusers = db.Column(db.Text, nullable=False, default='')
    community = db.Column(db.ForeignKey(Community.id, ondelete='CASCADE'), nullable=False)
    post_community = db.relationship(Community, passive_deletes=True,lazy="joined",
                                     backref=db.backref("community_posts", passive_deletes=True))

    def set_html_page(self, nhtml_page):
        self.html_page = nhtml_page

    def get_html_page(self):
        return self.html_page
