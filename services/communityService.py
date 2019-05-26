from datetime import datetime
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from sqlalchemy import update

mod = Blueprint('community', __name__)
from app import db
from models.user import User
from models.community import Community
from models.moderator import Moderator

@mod.route('/mycommunities', methods=['GET'])
def mycommunities():
    query = db.session.query(User).filter_by(username=session['name']).join(User.user_subscribe)
    data = query.first()
    if data != None:
        data =data.user_subscribe
    else:
        data =[]
    return render_template('mycommunities.html', communities=data)


@mod.route('/unsubscribecommunity', methods=['POST'])
def unsubscribecommunity():
    id = request.form['id']
    nuser = User.query.filter_by(id=session['user_id']).one()
    newcommunity = Community.query.filter_by(id=id).first()
    newcommunity.subscribe_user.remove(nuser)
    newcommunity.moderators_users.remove(nuser)
    db.session.add(newcommunity)
    db.session.commit()
    return redirect('/mycommunities')


@mod.route('/createcommunity', methods=['POST'])
def createcommunity():
    title = request.form['title']
    comtype = request.form['comtype']
    newcommunity = Community(title=title, type=comtype)
    db.session.add(newcommunity)
    nuser = User.query.filter_by(username=session['name']).first()
    db.session.commit()
    newcommunity = Community.query.filter_by(title=title).first()
    newcommunity.subscribe_user.append(nuser)
    newcommunity.moderators_users.append(nuser)
    db.session.add(newcommunity)
    session['com_id'] = newcommunity.id
    db.session.commit()
    return redirect('/mycommunities')
