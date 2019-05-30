from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update

mod = Blueprint('community', __name__)
from app import db
from models.user import User
from models.community import Community
from models.post import Post
from models.comment import Comment
from models.moderator import Moderator


@mod.route('/mycommunities', methods=['GET'])
def mycommunities():
    query = db.session.query(User).filter_by(username=session['name']).join(User.user_subscribe)
    data = query.first()
    if data != None:
        data = data.user_subscribe
    else:
        data = []
    return render_template('mycommunities.html', communities=data)


@mod.route('/unsubscribecommunity', methods=['POST'])
def unsubscribecommunity():
    id = request.form['id']
    nuser = User.query.filter_by(id=session['user_id']).one()
    newcommunity = Community.query.filter_by(id=id).first()
    newcommunity.subscribe_user.remove(nuser)
    newcommunity.moderators_users.remove(nuser)
    db.session.add(newcommunity)
    db.session.commit()
    return redirect('/mycommunities')


@mod.route('/createcommunity', methods=['POST'])
def createcommunity():
    title = request.form['title']
    comtype = request.form['comtype']
    newcommunity = Community(title=title, type=comtype)
    db.session.add(newcommunity)
    nuser = User.query.filter_by(username=session['name']).first()
    db.session.commit()
    newcommunity = Community.query.filter_by(title=title).first()
    newcommunity.subscribe_user.append(nuser)
    newcommunity.moderators_users.append(nuser)
    db.session.add(newcommunity)
    session['com_id'] = newcommunity.id
    db.session.commit()
    return redirect('/mycommunities')


@mod.route('/subscribecommunity', methods=['GET'])
def subscribecommunity():
    nuser = User.query.filter_by(id=session['user_id']).one()
    community = Community.query.filter_by(id=session['com_id']).first()
    community.subscribe_user.append(nuser)
    db.session.add(community)
    db.session.commit()
    return redirect('/community')


@mod.route('/community', methods=['GET'])
def community():
    st = request.args.get('val', '')
    if st != '':
        session['com_id'] = st
    query= Community.query.filter_by(id=session['com_id']).join(Community.community_posts, isouter=True).join(
        Comment, Comment.comid == session['com_id'] and Comment.postid == Post.id, isouter=True)
    community = query.first()
    return render_template('community.html', posts=community.community_posts, com=community)


@mod.route('/addpost', methods=['GET', 'POST'])
def addpost():
    if request.method == 'POST':
        id = request.form['id']
        community = Community.query.filter_by(id=session['com_id']).first()
        post = Post.query.filter_by(id=id).first()
        community.community_posts.append(post)
        db.session.add(community)
        db.session.commit()
        return redirect('/community')
    data = Post.query.filter_by(author=session['name']).order_by(Post.creation_date.desc()).all()
    return render_template("addpost.html", posts=data)
