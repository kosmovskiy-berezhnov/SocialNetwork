from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
from models import user, post
from sqlalchemy import update
from datetime import datetime
import os
mod = Blueprint('create_post', __name__)

@mod.route('/createposts', methods=['GET', 'POST'])
def createposts():
    from app import db
    if request.method == 'POST':
        html_page = request.form['html_page']
        title = request.form['title']
        newpost = post.Post(title, html_page,session['name'])
        db.session.add(newpost)
        db.session.commit()

    return render_template('createpost.html')

@mod.route('/addtext', methods=['POST'])
def addtext():
    from app import db
    return redirect('/createposts')

@mod.route('/addimage', methods=['POST'])
def addimage():
    from app import db
    file = request.files['pic']
    file.save(os.path.join(os.path.dirname(__file__), "static/images/", file.filename))
    str = '<p><img src="static/images/' + file.filename + '"width="auto" height="255"></p>\n'

    return redirect('/createposts')

@mod.route('/myposts', methods=['GET'])
def myposts():
    from app import db
    return render_template('myposts.html')