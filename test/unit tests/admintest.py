#!flask/bin/python
import unittest

from werkzeug.security import generate_password_hash

from config import db, create_app
from models.administrator import Administrator
from models.community import Community
from models.post import Post
from models.user import User
from services.notificationService import addNotification


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = create_app()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        user = User(username='nik',
                    password=generate_password_hash('nik'))
        db.session.add(user)
        user1 = User(username='dan',
                     password=generate_password_hash('dan'))
        db.session.add(user1)
        newcommunity = Community(title='com', type='public')
        user = User.query.filter_by(username='nik').first()
        newcommunity.moderators_users.append(user)
        newcommunity.subscribe_user.append(user)
        db.session.add(newcommunity)
        post = Post(title='mypost1', html_page='', author=user.username, community=1, rating=2)
        db.session.add(post)
        post = Post(title='mypost2', html_page='', author=user.username, community=1)
        db.session.add(post)
        db.session.commit()
        self.client = self.app.test_client()

    def create_newsletter(self):
        addNotification('nik', 'aaa')
        addNotification('dan', 'aaa')
        usernotif = User.query.filter_by(username='nik').first().get_notifications()
        usernotif2 = User.query.filter_by(username='dan').first().get_notifications()
        assert usernotif is not None and usernotif2 is not None

    def appoint_admin(self):
        ad = Administrator(username='nik')
        db.session.add(ad)
        db.session.commit()
        data = Administrator.query.all()
        assert len(data) == 2


if __name__ == '__main__':
    unittest.main()
