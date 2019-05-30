import os
from flask import Flask, Blueprint, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from forms import RegisterForm
from app import db
from models.user import User

mod = Blueprint('registration', __name__)


@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data.lower()).first()
        if user is None:
            user = User(username=form.login.data.lower(),
                        password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully')
            return redirect('/login')
        flash('User with this nickname already exists')

    return render_template("registration.html", form=form)
