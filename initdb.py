from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI
from werkzeug.security import generate_password_hash

from models.administrator import Administrator
from models.swagger_init import expose
from models.user import User


def init():
    from config import db
    from models import user,post,community,administrator,comment,moderator
    from models.user import User

    u = db.session.query(User).all()
    if len(u) > 0:
        u.remove(u[0])
        db.session.commit()
    a = db.session.query(Administrator).all()
    if len(a) > 0:
        a.remove(a[0])
        db.session.commit()
    # db.drop_all()
    # db.session.commit()
    db.create_all()
    db.session.commit()
    u = db.session.query(User).all()
    if len(u) > 0:
        u.remove(u[0])
    db.session.commit()



if __name__ == '__main__':
    from swagger_config import db, app
    init()
    db = SQLAlchemy(app)
    db.session.commit()
    user = User(username="admin1", password=generate_password_hash('admin1'))
    db.session.commit()
    admin = Administrator(user_id=1)
    # db.session.add(admin)
    db.session.commit()
