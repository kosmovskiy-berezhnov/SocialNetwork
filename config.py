from cryptography.fernet import Fernet
from flask import Flask
from flask import g
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI, SAFRSBase

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)
url_address = '127.0.0.1'

port = 5000
# db = SQLAlchemy(app)

db = SQLAlchemy()

lm = LoginManager()
lm.login_view = 'authorization.login'


def init():
    from werkzeug.security import generate_password_hash
    db.drop_all()
    from models.user import User
    from models.administrator import Administrator
    db.create_all()
    user = User(username="admin",
                password=generate_password_hash("admin"))

    admin = Administrator(username="admin")
    db.session.commit()


@lm.user_loader
def get_user(ident):
    from models.user import User
    return User.query.get(int(ident))


def create_api(app):
    SAFRSBase.db_commit = False
    api = SAFRSAPI(app, host=url_address, port=5000, prefix='/api/docs')
    from models import swagger_init
    swagger_init.expose(api)


def create_app():
    app = Flask(__name__)
    app.config.update(DEBUG=True, SECRET_KEY='secretkey',
                      USERNAME='admin', PASSWORD='admin')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    lm.init_app(app=app)
    from services import notificationService
    from services import content_creationService
    from services import registrationService
    from services import authorizationService
    from services import communityService
    from services import userService
    from services import adminService
    from services import moderatorService
    from services import sortService
    from services import checkcontentService
    app.register_blueprint(notificationService.mod)
    app.register_blueprint(content_creationService.mod)
    app.register_blueprint(registrationService.mod)
    app.register_blueprint(authorizationService.mod)
    app.register_blueprint(communityService.mod)
    app.register_blueprint(userService.mod)
    app.register_blueprint(moderatorService.mod)
    app.register_blueprint(adminService.mod)
    app.register_blueprint(sortService.mod)
    app.register_blueprint(checkcontentService.mod)
    with app.app_context():
        #init()
        create_api(app)

    @app.before_request
    def before_request():
        g.user = current_user
        g.id = 0 if not g.user.is_authenticated else g.user.id

    return app
