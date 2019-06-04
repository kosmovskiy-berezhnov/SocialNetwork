from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI
from werkzeug.security import generate_password_hash

from models.swagger_init import expose


def us():
    from models.user import User
    user = User(username="admin1", password=generate_password_hash('admin1'))
    return user

def init():
    from config import db
    from models import user,post,community,administrator,comment,moderator
    from models.user import User
    db.drop_all()
    db.session.commit()
    api = SAFRSAPI(app, host='127.0.0.1', port=5000, prefix='/api/docs')
    app.app_context().push()
    expose(api)
    db.create_all()
    db.session.commit()
    db = SQLAlchemy(app)
    db.session.commit()


if __name__ == '__main__':
    from config import db, app

    init()
