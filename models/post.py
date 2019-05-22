from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from user import user_post

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    html_page = db.Column(db.Text)
    posts = db.relationship("User", secondary=user_post, backpopulates='users')
    comments = None

    def __init__(self,title,html_page,author):
        self.title=title
        self.html_page=html_page
        self.creation_date=datetime.now()
        self.author = author
    def set_html_page(self, nhtml_page):
        self.html_page = nhtml_page

    def get_html_page(self):
        return html_page
db.create_all()