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

    def likepost(self):
        post = db.session.query(Post).filter_by(title='mypost2').one()
        post.rating = post.rating + 1
        db.session.commit()
        post = db.session.query(Post).filter_by(title='mypost2').one()
        assert post.rating == 1

    def likeandcheck(self):
        post = db.session.query(Post).filter_by(title='mypost1').one()
        post.rating = post.rating + 1
        post.evaluatedusers = 'nik'
        db.session.commit()
        post = db.session.query(Post).filter_by(title='mypost1').one()
        assert post.rating == 3 and post.evaluatedusers == 'nik'


if __name__ == '__main__':
    unittest.main()
