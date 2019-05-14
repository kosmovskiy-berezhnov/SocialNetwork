import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
db = SQLAlchemy(app)

from models import user

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    # session.pop('logged_in', None)
    if request.method == 'POST':
        _name = request.form['username']
        _password = request.form['password']
        data = user.User.query.filter_by(username=_name).all()
        if data != []:
            flash('This username has already exist!')
            return render_template('registration.html')
        else:
            flash('Success')
            reg = user.User(_name, _password)
            db.session.add(reg)
            db.session.commit()
            session['logged_in'] = True
            session['name'] = _name
            return render_template('home.html')
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _name = request.form['username']
        _password = request.form['password']
        data = user.User.query.filter_by(username=_name).all()
        if data == [] or not data[0].checkPas(_password):
            flash('Invalid username or password ')
        else:
            session['logged_in'] = True
            session['name'] = _name
            flash('You were logged in')
            return render_template('home.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('home.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
