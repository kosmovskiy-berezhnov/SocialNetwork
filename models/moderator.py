from safrs import SAFRSBase
from config import db


class Moderator(SAFRSBase, db.Model):
    '''
        description: mod
    '''
    mod_id = db.Column('mod_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    com_id = db.Column('com_id', db.Integer, db.ForeignKey('community.id'), primary_key=True)
