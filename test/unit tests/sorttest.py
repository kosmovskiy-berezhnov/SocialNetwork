#!flask/bin/python
import unittest

from werkzeug.security import generate_password_hash


from models.community import Community
from models.post import Post
from models.user import User
from config import db, create_app

class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = create_app()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        user = User(username='nik',
                    password=generate_password_hash('nik'))
        db.session.add(user)
        newcommunity = Community(title='com', type='public')
        db.session.add(newcommunity)
        post = Post(title='mypost1', html_page='', author=user.username, community=1, rating=2)
        db.session.add(post)
        post = Post(title='mypost2', html_page='', author=user.username, community=1)
        db.session.add(post)
        db.session.commit()
        self.client = self.app.test_client()


    def testtop(self):
        data = Post.query.filter_by(community=1).order_by(Post.rating.desc()).all()
        assert data[1].title == 'mypost2' and data[0].title == 'mypost1'
    def testnew(self):
        data = Post.query.filter_by(community=1).order_by(Post.creation_date.desc()).all()
        assert data[0].title=='mypost2' and data[1].title=='mypost1'


if __name__ == '__main__':
    unittest.main()
