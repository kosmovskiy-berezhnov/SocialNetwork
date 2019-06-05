from models.comment import Comment
from models.community import Community
from models.moderator import Moderator
from models.post import Post
from models.user import User
from models.administrator import Administrator


def expose(api):
    api.expose_object(User)
    api.expose_object(Moderator)
    api.expose_object(Post)
    api.expose_object(Community)
    api.expose_object(Comment)
    api.expose_object(Administrator)
