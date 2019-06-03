from safrs import SAFRSBase

from config import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

from models.comment import Comment
from models.user import User


class Post(SAFRSBase, db.Model):
    '''
        description: Post
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    html_page = db.Column(db.Text)
    author = db.Column(db.ForeignKey(User.username), nullable=False)
    authorrel = db.relationship(User, lazy="joined", backref="authorrel", cascade='all,delete')
    post_comments = db.relationship(Comment, cascade='all,delete',
                                    backref=db.backref("comment_post", cascade='all,delete'))
    evaluatedusers = db.Column(db.Text, nullable=False, default='')

    def set_html_page(self, nhtml_page):
        self.html_page = nhtml_page

    def get_html_page(self):
        return self.html_page
