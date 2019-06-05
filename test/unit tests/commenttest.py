#!flask/bin/python
import unittest

from werkzeug.security import generate_password_hash


from models.community import Community
from models.comment import Comment
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
        com = Comment(author=user.username, text='xaxa', postid=1)
        db.session.add(com)
        db.session.add(post)
        db.session.commit()
        self.client = self.app.test_client()


    def commentcheck(self):
        data = Post.query.filter_by(id=1).one()
        assert len(data.post_comments) == 1 and data.post_comments[0].text=='xaxa'

    def likecomment(self):
        comment = db.session.query(Comment).filter_by(id=1).one()
        comment.rating = comment.rating + 1
        db.session.commit()
        comment = db.session.query(Comment).filter_by(id=1).one()
        assert comment.rating==1

    def addcomment(self):
        com = Comment(author='nik', text='aaa', postid=2)
        db.session.add(com)
        db.session.commit()
        data = Post.query.filter_by(id=2).one()
        assert len(data.post_comments) == 1 and data.post_comments[0].text=='aaa'

    def deletecomment(self):
        com = db.session.query(Comment).filter_by(text='xaxa').delete()
        db.session.commit()
        data = Post.query.filter_by(id=1).one()
        assert len(data.post_comments)==0


if __name__ == '__main__':
    unittest.main()
