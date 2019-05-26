import os
from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy

from app import db
from models.user import User

mod = Blueprint('registration', __name__)


@mod.route('/reg', methods=['GET', 'POST'])
def reg():
    session.pop('logged_in', None)
    if request.method == 'POST':
        _name = request.form['username']
        _password = request.form['password']
        data = User.query.filter_by(username=_name).all()
        if data != []:
            flash('This username has already exist!')
            return render_template('registration.html')
        else:
            flash('Success')
            reg = User(username=_name, password=_password)
            db.session.add(reg)
            db.session.commit()
            session['user_id'] = User.query.filter_by(username=_name).first().id
            session['logged_in'] = True
            session['name'] = _name
            return render_template('home.html')
    return render_template('registration.html')
