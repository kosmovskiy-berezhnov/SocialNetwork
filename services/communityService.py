from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from flask_login import login_required

mod = Blueprint('community', __name__)
from config import db
from models.user import User
from models.community import Community
from models.post import Post
from models.comment import Comment
from models.moderator import Moderator


def check_community(community_name):
    community = Community.query.filter_by(title=community_name).first()
    return community


def is_subscribed(user_id, community_id):
    user = User.query.get(user_id)
    com = Community.query.filter_by(id=community_id).join(Community.subscribers).filter_by(id=user_id).first()
    return com is not None


def is_moderator(user_id, community_id):
    moderator = Moderator.query.filter_by(mod_id=user_id, com_id=community_id).first()
    return moderator is not None


@mod.route('/mycommunities', methods=['GET'])
@login_required
def mycommunities():
    data = None
    if session['admin'] == False:
        query = db.session.query(User).filter_by(username=g.user.username).join(User.communities).limit(100)
        data = query.first()
        if data != None:
            data = data.communities
        else:
            data = []
    else:
        data = Community.query.all()
    return render_template('mycommunities.html', communities=data)


@mod.route('/unsubscribecommunity', methods=['GET'])
@login_required
def unsubscribecommunity():
    user = db.session.query(User).filter_by(id=g.user.id).one()
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    community.subscribe_user.remove(user)
    if user in community.moderators_users:
        community.moderators_users.remove(user)
    db.session.commit()
    return redirect('/mycommunities')


@mod.route('/createcommunity', methods=['POST'])
@login_required
def createcommunity():
    title = request.form['title']
    comtype = request.form['comtype']
    if check_community(title) is not None:
        flash('community with such name already exists')
    else:
        nuser = db.session.query(User).filter_by(username=g.user.username).first()
        newcommunity = Community(title=title, type=comtype)
        # db.session.add(newcommunity)
        newcommunity.subscribers.append(nuser)
        newcommunity.mods.append(nuser)
        session['com_id'] = newcommunity.id
        db.session.commit()
        return redirect(url_for('community.concrete_community', community_name=newcommunity.title))
    return redirect('/mycommunities')


@mod.route('/subscribecommunity', methods=['GET'])
@login_required
def subscribecommunity():
    user = db.session.query(User).filter_by(id=session['user_id']).one()
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    community.subscribers.append(user)
    user.subscribe(community)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    community = community
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/com/<community_name>')
def concrete_community(community_name):
    query = db.session.query(Community).filter_by(title=community_name).join(Community.posts, isouter=True)
    community = query.first()
    if community is not None:
        if community.type == 'private' and g.user not in community.subscribers:
            flash('It is private community')
        else:
            session['com_id'] = community.id
            query = query.join(Comment, Comment.post_id == Post.id, isouter=True)
            community = query.first()
            is_subbed = False
            moder = False
            if not g.user.is_anonymous:
                is_subbed = is_subscribed(g.user.id, community.id)
                moder = is_moderator(g.user.id, community.id)
            return render_template('community.html', posts=community.posts, com=community,
                                   is_subbed=is_subbed, iscom=True, moder=moder)
    else:
        flash('community with such name does not exists')
    return redirect(url_for('community.allcommunities'))


@mod.route('/addpost', methods=['GET'])
@login_required
def addpost():
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    post = db.session.query(Post).filter_by(id=session['created_post']).first()
    community.community_posts.append(post)
    db.session.commit()
    session.pop('created_post', None)
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/deletepost', methods=['POST'])
@login_required
def deletepost():
    postid = request.form['postid']
    post = Post.query.filter_by(id=postid).first()
    community = Community.query.filter_by(id=session['com_id']).first()
    if session['admin'] == True or post.author == g.user.username or g.user in community.moderators_users:
        db.session.query(Post).filter_by(id=postid).delete()
        db.session.commit()
        flash("Post deleted")
    else:
        flash('Permission denied!')
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/', methods=['GET'])
def allcommunities():
    query = Community.query.filter(type != 'private').join(Community.posts, isouter=True).order_by(
        Post.id.desc())
    data = query.all()
    ans = []
    for com in data:
        if com.posts != []:
            post = sorted(com.posts, key=lambda x: x.creation_date, reverse=True)[0]
            ans.append((com, post))
    return render_template("home.html", communities=ans)


@mod.route('/allpeople', methods=['GET'])
def allpeople():
    query = db.session.query(User.username).filter(
        User.id == Moderator.mod_id and Moderator.com_id == session['com_id'])
    moderators = query.all()
    users = db.session.query(User).join(User.communities).filter_by(id=session['com_id']).all()
    return render_template("allpeople.html", moderators=moderators, users=users)
