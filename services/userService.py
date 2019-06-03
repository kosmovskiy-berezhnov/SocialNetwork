import os
from flask import Blueprint, Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy

from config import db
from models.comment import Comment
from models.post import Post
from models.user import User

mod = Blueprint('userService', __name__)


@mod.route('/addcomment', methods=['POST'])
def addcomment():
    postid = request.form['postid']
    text = request.form['text']
    com = Comment(author=session['name'], comid=session['com_id'], text=text, postid=postid)
    db.session.add(com)
    db.session.commit()
    return redirect('/community')


@mod.route('/likepost', methods=['POST'])
def likepost():
    postid = request.form['postid']
    post = Post.query.filter_by(id=postid).one()
    users = post.evaluatedusers.split(',')
    ok = False
    for i in range(0, len(users)):
        if session['name'] == users[i]:
            ok = True
            break
    if ok:
        flash('You have already rated')
    else:
        post.rating = post.rating + 1
        post.evaluatedusers = session['name'] + ',' + post.evaluatedusers
        Post.query.filter_by(id=postid).update({"evaluatedusers": post.evaluatedusers, "rating": post.rating})
        db.session.commit()
    return redirect('/community')
