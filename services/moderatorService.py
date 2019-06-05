from cryptography.fernet import Fernet
from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json
from flask_login import login_required
import base64
from config import db, cipher
from models.administrator import Administrator
from models.comment import Comment
from models.community import Community
from models.moderator import Moderator
from models.post import Post
from models.user import User

mod = Blueprint('moderator', __name__)



@mod.route('/appointmoderator', methods=['POST'])
@login_required
def appointmoderator():
    username = request.form['username']
    user = db.session.query(User).filter_by(username=username)
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    if user in community.subscribe_user:
        flash('moderator assigned!')
        if user not in community.moderators_users:
            community.moderators_users.append(user)
            db.session.commit()
    else:
        flash('This user is not subscribed to the community!')
    return redirect(url_for('community.concrete_community, community_name=' + community.title))


@mod.route('/deletecommunity', methods=['POST'])
@login_required
def deletecommunity():
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    if session['admin'] == True or (g.user in community.moderators_users and community != 'public'):
        flash('community deleted!')
        db.session.query(Community).filter_by(id=session['com_id']).delete()
        db.session.commit()
    else:
        flash("Permission denied")
    return redirect(url_for('community.allcommunities'))


@mod.route('/banuser', methods=['POST'])
@login_required
def banuser():
    username = request.form['username']
    user = db.session.query(User).filter_by(username=username).first()
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    if user is None or user not in community.subscribe_user:
        flash("This user are not subscribe for this community")
    else:
        flash("User are baned")
        data = community.banned_users
        data.append(user.username)
        community.banned_users=data
        db.session.add(community)
        db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/unbanuser', methods=['POST'])
@login_required
def unbanuser():
    username = request.form['username']
    user = db.session.query(User).filter_by(username=username).first()
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    if user is None or user not in community.subscribe_user:
        flash("This user are not subscribe for this community")
    else:
        flash("User are unbaned")
        community.banned_users.remove(user.username)
        db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/deleteuser', methods=['POST'])
@login_required
def deleteuser():
    flash('user deleted from the community!')
    username = request.form['username']
    user = db.session.query(User).filter_by(username=username).first()
    community = db.session.query(Community).filter_by(id=session['com_id']).first()
    if community.type != "private":
        flash("You can delete user from only private community")
    elif user is None or user not in community.subscribe_user:
        flash("This user are not subscribe for this community")
    elif session['admin'] == False and user in community.moderators_users:
        flash("You cannot delete moderator!")
    else:
        community.subscribe_user.remove(user)
        db.session.commit()
    return redirect(url_for('community.concrete_community', community_name=community.title))


@mod.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if request.method == 'POST':
        username = request.form['username']
        user = db.session.query(User).filter_by(username=username).first()
        community = db.session.query(Community).filter_by(id=session['com_id']).first()
        if user is None:
            flash("This user are not exist")
        elif user in community.subscribe_user:
            flash("This user are subscribe for this community")
        else:
            from services.notificationService import addNotification
            b = g.user.password[20:52].encode()
            cipher_key = base64.urlsafe_b64encode(b)
            cipher = Fernet(cipher_key)
            text=(community.title+':'+user.username).encode()
            encrypted_text = cipher.encrypt(text)
            encrypted_text=encrypted_text.decode()
            notification = '<p><font color ="green">Invitation for community ' + community.title + '</font></p>' + \
                           '<a href ='+ url_for("moderator.adduser")+'?comid='+ encrypted_text +'&mod='+g.user.username+'>Subscribe</a>'
            addNotification(user.username, notification)
        return redirect(url_for('community.concrete_community', community_name=community.title))
    else:
        mod = request.args.get('mod', '')
        moder = db.session.query(User).filter_by(username=mod).first()
        if moder is None:
            flash('Permission denied')
        else:
            com =request.args.get('comid', '').encode()
            b = moder.password[20:52].encode()
            cipher_key = base64.urlsafe_b64encode(b)
            cipher = Fernet(cipher_key)
            decrypted_text = cipher.decrypt(com, ttl=None)
            comtitle, username = decrypted_text.decode().split(':')
            community = db.session.query(Community).filter_by(title=comtitle).first()
            if community is None or username!=g.user.username:
                flash('Permission denied')
            else:
                flash('You subscribe!')
                community.subscribe_user.append(g.user)
                # db.session.add(community)
                db.session.commit()
                return redirect(url_for('community.concrete_community', community_name=community.title))
        return redirect(url_for('community.allcommunities'))

