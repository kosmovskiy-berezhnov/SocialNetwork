import os
from flask import Blueprint, Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user
from forms import LoginForm
from werkzeug.security import check_password_hash
from config import db
from models.user import User
mod = Blueprint('authorization', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("main_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data.lower()).first()
        if user is None:
            flash("No user with such nickname")
        elif check_password_hash(user.password, form.password.data):
            login_user(user)
            global current_id
            current_id = user.id
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Wrong password')
    return render_template('login.html', form=form)


@mod.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return render_template('home.html')
