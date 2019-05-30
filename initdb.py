
def init():
    from app import db
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    init()