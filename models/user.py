from models.community import Community


class User:
    def __init__(self):
        self._username
        self._password
        self._rating
        self._communities
        self._notifications

    def get_username(self):
        return self._username

    def get_rating(self):
        pass

    def change_rating(self):
        pass

    def subscribe(self, community: Community):
        pass
