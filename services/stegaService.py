from flask import Blueprint
from stegano import lsbset
from stegano.lsbset import generators
from time import time

mod = Blueprint('stega', __name__)

path_to_pics = "static/images/"
separator = ' '


def hide_author(user, pic_name):
    message = user.username + separator + str(time())
    new_file = str(hash(pic_name)) + '.png'
    secret = lsbset.hide(path_to_pics + pic_name, message, generators.eratosthenes())
    path = path_to_pics + new_file
    secret.save(path)
    return new_file


def find_message(pic_name):
    try:
        mess = lsbset.reveal(path_to_pics + pic_name, generators.eratosthenes())
    except IndexError:
        return False
    return mess
