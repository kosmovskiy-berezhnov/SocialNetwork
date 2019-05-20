from datetime import datetime


class Notification:

    def __init__(self, username, text, creation_date):
        self.text = text
        self.creation_date = creation_date
        self.username = username

    def toJSON(self):
        return {'text': self.text,
                                'username': self.username,
                                 'creation_date': self.creation_date}