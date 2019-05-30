from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update

mod = Blueprint('community', __name__)
from app import db
from models.user import User
from models.community import Community
from models.post import Post
from models.moderator import Moderator


@mod.route('/mycommunities', methods=['GET'])
def mycommunities():
    query = db.session.query(User).filter_by(username=g.user.username).join(User.user_subscribe)
    data = query.first()
    if data != None:
        data = data.user_subscribe
    else:
        data = []
    return render_template('mycommunities.html', communities=data)


@mod.route('/unsubscribecommunity', methods=['POST'])
def unsubscribecommunity():
    id = request.form['id']
    nuser = User.query.filter_by(id=g.user.id).one()
    newcommunity = Community.query.filter_by(id=id).first()
    newcommunity.subscribe_user.remove(nuser)
    newcommunity.moderators_users.remove(nuser)
    db.session.add(newcommunity)
    db.session.commit()
    return redirect('/mycommunities')


def check_community(community_name):
    community = Community.query.filter_by(title=community_name).first()
    return community


def is_subscribed(user_id, community_id):
    com = Community.query.get(community_id)
    user = com.subscribe_user.filter_by(id=user_id).first()
    return user is not None



@mod.route('/createcommunity', methods=['POST'])
def createcommunity():
    title = request.form['title']
    comtype = request.form['comtype']
    if check_community(title) is not None:
        flash('community with this name already exists')
    else:
        newcommunity = Community(title=title, type=comtype)
        db.session.add(newcommunity)
        nuser = User.query.filter_by(username=g.user.username).first()
        db.session.commit()
        newcommunity = Community.query.filter_by(title=title).first()
        newcommunity.subscribe_user.append(nuser)
        newcommunity.moderators_users.append(nuser)
        db.session.add(newcommunity)
        session['com_id'] = newcommunity.id
        db.session.commit()
        return render_template('community.html', posts=newcommunity.community_posts, com=newcommunity,
                               is_subbed=is_subscribed(g.user, newcommunity))
    return redirect('/mycommunities')


@mod.route('/subscribecommunity', methods=['GET'])
def subscribecommunity():
    nuser = User.query.filter_by(id=session['user_id']).one()
    community = Community.query.filter_by(id=session['com_id']).first()
    community.subscribe_user.append(nuser)
    db.session.add(community)
    db.session.commit()
    return redirect('/community')


@mod.route('/com/<community_name>')
def concrete_community(community_name):
    community = Community.query.filter_by(title=community_name).join(Community.community_posts, isouter=True).first()
    if community is not None:
        return render_template('community.html', posts=community.community_posts, com=community,
                               is_subbed=is_subscribed(g.user.id, community.id))
    flash('community with such name does not exists')
    redirect('/community')


@mod.route('/community', methods=['GET'])
def community():
    st = request.args.get('val', '')
    if st != '':
        session['com_id'] = st
    community = Community.query.filter_by(id=session['com_id']).join(Community.community_posts, isouter=True).first()
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
    data = Post.query.filter_by(author=g.user.username).order_by(Post.creation_date.desc()).all()
    return render_template("addpost.html", posts=data)
