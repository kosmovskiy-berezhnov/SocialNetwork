from models.community import Community
from models.moderator import Moderator
from models.post import Post
from .user import User


def expose(api):
    api.expose_object(User)
    api.expose_object(Moderator)
    api.expose_object(Post)
    api.expose_object(Community)
