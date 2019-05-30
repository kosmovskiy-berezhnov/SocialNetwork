import os
from flask import Blueprint, Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from app import db
from forms import LoginForm
from models.user import User

mod = Blueprint('authorization', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data.lower()).first()
        if user is None:
            flash("No user with such nickname")
        elif check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Wrong password')
    return render_template('login.html', form=form)


@mod.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return render_template('home.html')
