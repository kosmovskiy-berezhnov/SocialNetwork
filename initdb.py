from werkzeug.security import generate_password_hash


def init():
    from config import db

    from models.user import User
    from models.administrator import Administrator
    db.create_all()
    user = User(username="admin",
                password=generate_password_hash("admin"))
    db.session.add(user)
    admin = Administrator(username="admin")
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    from config import db
    db.drop_all()
    #init()
