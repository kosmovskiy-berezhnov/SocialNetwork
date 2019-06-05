import os
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, json

from services.stegaService import find_message

mod = Blueprint('checkcontent', __name__)


def check_image(filename):
    if os.path.exists(os.path.join(os.path.split(os.path.dirname(__file__))[0], "static/images/", filename)):
        mess = find_message(filename)
        if mess:
            return mess
    return False


@mod.route('/checkimage', methods=['POST'])
def checkimage():
    file = request.files['pic']
    answer = check_image(file.filename)
    if answer:
        flash("Not unique content, was made by " + answer)

    else:
        flash("This image is unique!")
    return redirect('/')
