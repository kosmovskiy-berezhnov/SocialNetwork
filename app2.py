import os
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.drop_all()


class Moderator(db.Model):
    mod_id = db.Column('mod_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    com_id = db.Column('com_id', db.Integer, db.ForeignKey('community.id'), primary_key=True)


class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    banned_users = None
    # subscribe_table = db.Table('subscribeUsers', db.metadata,
    #                            db.Column('com_id', db.Integer, db.ForeignKey(id), primary_key=True),
    #                            db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
    #                            )
    subscribe_user = db.relationship('User', secondary='moderator', cascade='all,delete',
                                     primaryjoin=Moderator.com_id == id,
                                     backref=db.backref("user_subscribe", cascade='all,delete'),
                                     )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(30), nullable=False)
    notifications = db.Column(JSON, nullable=True)


db.create_all()


@app.route('/')
def home():
    newcommunity = Community(title='nana', type='xaxa')
    nuser = User(username='nik', password='nik')
    db.session.add(nuser)
    #newcommunity = newcommunity.subscribe_user.append(nuser)

    db.session.add(newcommunity)
    db.session.commit()
    nuser= User.query.filter_by(username='nik').first()
    newcommunity = Community.query.filter_by(title='nana').first()

    newcommunity.subscribe_user.append(nuser)
    db.session.add(newcommunity)
    #db.session.add(Moderator(mod_id =1,com_id = 1))
    db.session.commit()
    return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
