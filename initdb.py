from werkzeug.security import generate_password_hash
from models.administrator import Administrator
from models import user


def init():
    from config import db
    db.session.close()
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()


def make_admin():
    from swagger_config import db
    db.session.commit()
    u = user.User(username="admin1", password=generate_password_hash('admin1'))
    admin = Administrator(user_id=1)
    db.session.commit()

if __name__ == '__main__':
    from config import db
    init()
    db.session.commit()
    make_admin()
    db.session.commit()
    a = db.session.query(Administrator).all()
