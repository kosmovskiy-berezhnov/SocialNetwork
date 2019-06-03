from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json

from config import db
from models.administrator import Administrator
from models.comment import Comment
from models.community import Community
from models.moderator import Moderator
from models.post import Post
from models.user import User

mod = Blueprint('sort', __name__)


@mod.route('/sort', methods=['GET'])
def sort():
    from communityService import is_moderator, is_subscribed
    community = Community.query.filter_by(id=session['com_id']).first()
    type = request.form['sort']
    data = None
    if type == 'new':
        data = Post.query.filter_by(commmunity=session['com_id']).join(Comment, Comment.postid == Post.id,
                                                                       isouter=True).order_by(
            Post.creation_date.desc()).all()
    elif type == 'top':
        data = Post.query.filter_by(commmunity=session['com_id']).join(Comment, Comment.postid == Post.id,
                                                                       isouter=True).order_by(Post.rating.desc()).all()
    is_subbed = False
    moder = False
    if not g.user.is_anonymous:
        is_subbed = is_subscribed(g.user.id, community.id)
        moder = is_moderator(g.user.id, community.id)
    return render_template('community.html', posts=data, com=community, is_subbed=is_subbed, iscom=True, moder=moder)
