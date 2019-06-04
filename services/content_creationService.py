import os
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from config import db, url_address
from flask_login import login_required
from models.post import Post
from models.community import Community
mod = Blueprint('create_post', __name__)


@mod.route('/createposts', methods=['GET', 'POST'])
@login_required
def createposts():
    community = Community.query.filter_by(id=session['com_id']).first()
    if community.type =='personal' and g.user not in community.moderators_users:
        flash('You cannot create post in this community')
        return redirect(url_for('community.allcommunities'))
    else:

        if request.method == 'POST':
            html_page = ''
            if 'html_page' in dict(request.files):
                file = request.files['html_page']
                str = file.filename.split('.')
                if len(str) < 2 or str[len(str) - 1] != 'html':
                    flash('Uncorrect format!')

                    return redirect(url_for('community.concrete_community', community_name=community.title))
                html_page = file.read().decode("utf-8")
            title = request.form['title']
            newpost = Post(title=title, html_page=html_page, author=g.user.username, community=session['com_id'])
            # db.session.add(newpost)
            db.session.commit()
            pid = Post.query.filter_by(author=g.user.username).order_by(Post.creation_date.desc()).first().id
            session['created_post'] = pid
        post = Post.query.filter_by(id=session['created_post']).first()
        return render_template('createpost.html', post=post)


@mod.route('/addtext', methods=['POST'])
@login_required
def addtext():
    text = request.form['text']
    text = '<p>' + text + '</p>'
    post = Post.query.filter_by(id=session['created_post']).first()
    post.html_page = post.html_page + text
    Post.query.filter_by(id=session['created_post']).update({"html_page": post.html_page})
    db.session.commit()
    return redirect('/createposts')


@mod.route('/addimage', methods=['POST'])
@login_required
def addimage():
    file = request.files['pic']
    file.save(os.path.join(os.path.split(os.path.dirname(__file__))[0], "static/images/", file.filename))
    str = '<p><img src="http://'+url_address + '/static/images/' + file.filename + '"width="auto" height="255"></p>\n'
    post = Post.query.filter_by(id=session['created_post']).first()
    post.html_page = post.html_page + str
    Post.query.filter_by(id=session['created_post']).update({"html_page": post.html_page})
    db.session.commit()
    return redirect('/createposts')


@mod.route('/myposts', methods=['GET'])
@login_required
def myposts():
    data = Post.query.filter_by(author=g.user).order_by(Post.creation_date.desc()).all()
    return render_template('myposts.html', posts=data)
