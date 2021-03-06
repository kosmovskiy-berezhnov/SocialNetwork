from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update
from flask_login import login_required
mod = Blueprint('notifications', __name__)
from config import db
from models.user import User
from models.notification import Notification
from flask_login import current_user, login_required, login_user


def addNotification(name, notification):
    user = db.session.query(User).filter_by(username=name).first()
    data = user.get_notifications()
    n = Notification(g.user.username, notification, datetime.now().replace(microsecond=0))

    if data == '[]':
        data = "[" + json.dumps(n.toJSON()) + "]"
    else:
        data = '[' + json.dumps(n.toJSON()) + ',' + data[1:]
    user.notifications=data
    db.session.commit()


@mod.route('/mypage', methods=['GET'])
@login_required
def mypage():
    data = User.query.filter_by(username=g.user.username).first().get_notifications()
    notif = None
    if data != None:
        notif = json.loads(data)
    return render_template('mypage.html', notifications=notif)


@mod.route('/deleteNotification', methods=['POST'])
@login_required
def deleteNotification():
    user = db.session.query(User).filter_by(username=g.user.username).first()
    data = user.get_notifications()
    username = request.form['username']
    creation_date = request.form['creation_date']
    text = request.form['text']
    data = User.query.filter_by(username=g.user.username).all()
    notif = json.loads(data[0].get_notifications())
    for i in range(0, len(notif)):
        if username == notif[i]['username'] and creation_date == notif[i]['creation_date'] and text == notif[i]['text']:
            notif.remove(notif[i])
            break
    jsonStr = json.dumps(notif)
    user.notifications = jsonStr
    db.session.commit()
    return redirect('/mypage')


@mod.route('/createNotification', methods=['POST'])
@login_required
def createNotification():
    name = request.form['username']
    user = User.query.filter_by(username=name).first()
    if user is None:
        flash("This user does not exist")
    else:
        notification = request.form['notification']
        addNotification(name, notification)
    return redirect('/mypage')
