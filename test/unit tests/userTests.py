#!flask/bin/python
import os
from flask import request, render_template, flash, g, session, redirect, url_for, json
from flask_login import login_required
from models.user import User
from models.community import Community
from models.post import Post
from models.comment import Comment
from models.moderator import Moderator
from models.administrator import Administrator

import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, url_address, port, create_app

class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = create_app()
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client()
       #app.run(host=url_address, port=port)

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        #db.drop_all()

    def test_exist(self):
        user = User.query.filter_by(username='dodo').first()
        assert user is None

    def admin_exist(self):
        admin = Administrator.query.all()
        assert len(admin) ==1

    def test_reg(self):
        user = User(username='nik',
                    password=generate_password_hash('nik'))
        db.session.add(user)
        db.session.commit()
        users = User.query.filter_by(username='nik').first()
        assert users is not None

    def hash_passwords(self):
        user = User.query.filter_by(username='nik').first()
        assert check_password_hash(user.password, 'nik')

if __name__ == '__main__':
    unittest.main()