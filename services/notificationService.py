from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update

mod = Blueprint('notifications', __name__)
from app import db
from models.user import User
from models.notification import Notification


@mod.route('/mypage', methods=['GET'])
def mypage():
    data = User.query.filter_by(username=g.user.username).first().get_notifications()
    notif = None
    if data != None:
        notif = json.loads(data)
    return render_template('mypage.html', notifications=notif)


@mod.route('/deleteNotification', methods=['POST'])
def deleteNotification():
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
    User.query.filter_by(username=g.user.username).update({"notifications": jsonStr})
    db.session.commit()
    return redirect('/mypage')


@mod.route('/createNotification', methods=['POST'])
def createNotification():
    name = request.form['username']
    notification = request.form['notification']
    data = User.query.filter_by(username=name).all()[0].get_notifications()
    n = Notification(g.user.username, notification, datetime.now())
    if data == None:
        data = "[" + json.dumps(n.toJSON()) + "]"
    else:
        data = '[' + json.dumps(n.toJSON()) + ',' + data[1:]
    User.query.filter_by(username=name).update({"notifications": data})
    db.session.commit()
    return redirect('/mypage')
