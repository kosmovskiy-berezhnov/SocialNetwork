from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from models import user
from models.notification import Notification
from sqlalchemy import update
from datetime import datetime
mod = Blueprint('notifications', __name__)

@mod.route('/mypage', methods=['GET'])
def mypage():
    data = user.User.query.filter_by(username=session['name']).all()[0].get_notifications()
    notif = None
    if data != None:
        notif = json.loads(data)
    return render_template('mypage.html', notifications=notif)

@mod.route('/deleteNotification', methods=['POST'])
def deleteNotification():
    from app import db
    username = request.form['username']
    creation_date = request.form['creation_date']
    text = request.form['text']
    data = user.User.query.filter_by(username=session['name']).all()
    notif = json.loads(data[0].get_notifications())
    for i in range(0,len(notif)):
        if username == notif[i]['username'] and creation_date == notif[i]['creation_date'] and text == notif[i]['text']:
            notif.remove(notif[i])
            break
    jsonStr = json.dumps(notif)
    user.User.query.filter_by(username=session['name']).update({"_notifications":  jsonStr})
    db.session.commit()
    return redirect('/mypage')


@mod.route('/createNotification', methods=['POST'])
def createNotification():
    from app import db
    name = request.form['username']
    notification = request.form['notification']
    data = user.User.query.filter_by(username=name).all()[0].get_notifications()
    n = Notification(session['name'], notification,datetime.now())
    if data == None:
        data = "[" + json.dumps(n.toJSON()) + "]"
    else:
        data = data[:-1] + ',' + json.dumps(n.toJSON()) + ']'
    user.User.query.filter_by(username=name).update({"_notifications": data})
    db.session.commit()
    return redirect('/mypage')
