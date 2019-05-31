import os
from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update
from app import current_user
from app import db
from models.post import Post
from models.user import User

mod = Blueprint('create_post', __name__)


@mod.route('/createposts', methods=['GET', 'POST'])
def createposts():
    if request.method == 'POST':
        html_page = ''
        if 'html_page' in dict(request.files):
            file = request.files['html_page']
            html_page = file.read().decode("utf-8")
        title = request.form['title']
        newpost = Post(title=title, html_page=html_page, author=g.user.username)
        db.session.add(newpost)
        db.session.commit()
        pid = Post.query.filter_by(author=g.user.username).order_by(Post.creation_date.desc()).first().id
        session['created_post'] = pid
    post = Post.query.filter_by(id=session['created_post']).first()
    return render_template('createpost.html', post=post)


@mod.route('/addtext', methods=['POST'])
def addtext():
    text = request.form['text']
    text = '<p>' + text + '</p>'
    post = Post.query.filter_by(id=session['created_post']).first()
    post.html_page = post.html_page + text
    Post.query.filter_by(id=session['created_post']).update({"html_page": post.html_page})
    db.session.commit()
    return redirect('/createposts')


@mod.route('/addimage', methods=['POST'])
def addimage():
    file = request.files['pic']
    file.save(os.path.join(os.path.split(os.path.dirname(__file__))[0], "static/images/", file.filename))
    str = '<p><img src="static/images/' + file.filename + '"width="auto" height="255"></p>\n'
    post = Post.query.filter_by(id=session['created_post']).first()
    post.html_page = post.html_page + str
    Post.query.filter_by(id=session['created_post']).update({"html_page": post.html_page})
    db.session.commit()
    return redirect('/createposts')


@mod.route('/myposts', methods=['GET'])
def myposts():
    data = Post.query.filter_by(author=g.user.username).order_by(Post.creation_date.desc()).all()
    return render_template('myposts.html', posts=data)
