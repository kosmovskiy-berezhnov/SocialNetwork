import os
from flask import Blueprint, Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from app import db
from models.user import User

mod = Blueprint('authorization', __name__)

@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _name = request.form['username']
        _password = request.form['password']
        data = User.query.filter_by(username =_name).all()
        if data == [] or not data[0].checkPas(_password):
            flash('Invalid username or password ')
        else:
            session['logged_in'] = True
            session['name'] = _name
            flash('You were logged in')
            return render_template('home.html')
    return render_template('login.html')


@mod.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('home.html')