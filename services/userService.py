import os
from flask import Blueprint, Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, logout_user
from config import db
from models.comment import Comment
from models.post import Post
from models.user import User
from models.community import Community
mod = Blueprint('userService', __name__)


@mod.before_request
def before_request():
    if 'com_id' in session:
        community = Community.query.filter_by(id=session['com_id']).first()
        if g.user in community.banned_users:
            flash("You are banned!")
            return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/addcomment', methods=['POST'])
@login_required
def addcomment():
    community = Community.query.filter_by(id=session['com_id']).first()
    postid = request.form['postid']
    text = request.form['text']
    com = Comment(author=g.user.username, text=text, postid=postid)
    db.session.add(com)
    db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/deletecomment', methods=['POST'])
@login_required
def deletecomment():
    community = Community.query.filter_by(id=session['com_id']).first()
    comid = request.form['comid']
    db.session.query(Comment).filter_by(id=comid).delete()
    db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/likepost', methods=['POST'])
@login_required
def likepost():
    community = Community.query.filter_by(id=session['com_id']).first()
    postid = request.form['postid']
    post = db.session.query(Post).filter_by(id=postid).one()
    users = post.evaluatedusers.split(',')
    ok = False
    for i in range(0, len(users)):
        if g.user.username == users[i]:
            ok = True
            break
    if ok:
        flash('You have already rated')
    else:
        post.rating = post.rating + 1
        val=db.session.query(db.func.avg(Post.rating)).filter_by(community=session['com_id']).first()
        community.rating = round(val[0])
        val=db.session.query(db.func.avg(Post.rating)).filter_by(author=post.author).first()
        user=db.session.query(User).filter_by(username=post.author).first()
        user.rating= round(val[0])
        post.evaluatedusers = g.user.username + ',' + post.evaluatedusers
        db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/likecomment', methods=['POST'])
@login_required
def likecomment():
    community = Community.query.filter_by(id=session['com_id']).first()
    comid = request.form['comid']
    comment = db.session.query(Comment).filter_by(id=comid).one()
    users = comment.evaluatedusers.split(',')
    ok = False
    for i in range(0, len(users)):
        if g.user.username == users[i]:
            ok = True
            break
    if ok:
        flash('You have already rated')
    else:
        comment.rating = comment.rating + 1
        comment.evaluatedusers = g.user.username + ',' + comment.evaluatedusers
        db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/deleteprofile', methods=['GET'])
@login_required
def deleteprofile():
    db.session.query(User).filter_by(id=g.user.id).delete()
    flash('Your profile are deleted!!')
    logout_user()
    session.clear()
    db.session.commit()
    return redirect(url_for('community.allcommunities'))
