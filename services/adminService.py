from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json

from config import db
from models.administrator import Administrator
from models.user import User

mod = Blueprint('admin', __name__)


@mod.route('/appointadmin', methods=['POST'])
def appointadmin():
    flash('admin assigned!')
    username = request.form['username']
    admin = Administrator(username=username)
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('community.allcommunities'))


@mod.route('/newsletter', methods=['POST'])
def newsletter():
    from services.notificationService import addNotification
    notification = request.form['notification']
    notification = '<p><font color ="red">Notification from admin:</font></p>' + notification
    users = User.query.outerjoin(Administrator).filter(Administrator.username.is_(None)).all()
    for user in users:
        addNotification(user.username, notification)
    return redirect(url_for('community.allcommunities'))
