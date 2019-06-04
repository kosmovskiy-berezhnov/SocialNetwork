from werkzeug.security import generate_password_hash


def init():
    from config import db
    from models import user,post,community,administrator,comment,moderator
    db.drop_all()
    db.create_all()
    user = user.User(username="admin",
                password=generate_password_hash("admin"))
    db.session.add(user)
    admin = administrator.Administrator(username="admin")
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    from config import db
    init()
