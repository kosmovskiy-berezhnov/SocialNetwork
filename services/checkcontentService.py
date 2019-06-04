import os
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json
mod = Blueprint('checkcontent', __name__)


def check_image(filename):
    return not os.path.exists(os.path.join(os.path.split(os.path.dirname(__file__))[0], "static/images/", filename))


@mod.route('/checkimage', methods=['POST'])
def checkimage():
    file = request.files['pic']
    if check_image(file.filename):
        flash("This image are unique!")
    else:
        flash("Not unique content")
    return redirect(url_for('community.allcommunities'))