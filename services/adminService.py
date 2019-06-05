from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json
from flask_login import login_required

from config import db
from models.administrator import Administrator
from models.user import User

mod = Blueprint('admin', __name__)


@mod.route('/appointadmin', methods=['POST'])
@login_required
def appointadmin():
    username = request.form['username']
    if User.query.filter_by(username=username).first() is None:
        flash('invalid user!')
    else:
        if Administrator.query.filter_by(username=username).first() is None:
            flash('admin assigned!')
            admin = Administrator(username=username)
            db.session.add(admin)
            db.session.commit()
        else:
            flash('admin has already been assigned!')
    return redirect(url_for('community.allcommunities'))


@mod.route('/newsletter', methods=['POST'])
@login_required
def newsletter():
    from services.notificationService import addNotification
    notification = request.form['notification']
    notification = '<p><font color ="red">Notification from admin:</font></p>' + notification
    users = User.query.outerjoin(Administrator).filter(Administrator.username.is_(None)).all()
    for user in users:
        addNotification(user.username, notification)
    return redirect(url_for('community.allcommunities'))


@mod.route('/administrators', methods=['GET'])
def administrators():
    admin = Administrator.query.all()
    return render_template("admin.html", admins=admin)
