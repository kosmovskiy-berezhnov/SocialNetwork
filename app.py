from flask import Flask, g
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app=app)
lm.login_view = 'authorization.login'

from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)


@lm.user_loader
def get_user(ident):
    from models.user import User
    return User.query.get(int(ident))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.before_request
def before_request():
    g.user = current_user
    g.id = 0 if not g.user.is_authenticated else g.user.id


@app.after_request
def after_request(response):
    db.session.close()
    return response


from services import notificationService
from services import content_creationService
from services import registrationService
from services import authorizationService
from services import communityService
from services import userService
from services import adminService
from services import moderatorService
from services import sortService

app.register_blueprint(notificationService.mod)
app.register_blueprint(content_creationService.mod)
app.register_blueprint(registrationService.mod)
app.register_blueprint(authorizationService.mod)
app.register_blueprint(communityService.mod)
app.register_blueprint(userService.mod)
app.register_blueprint(moderatorService.mod)
app.register_blueprint(adminService.mod)
app.register_blueprint(sortService.mod)
if __name__ == '__main__':
    try:
        app.debug = True
        app.run(host='127.0.0.1', port=5000, debug=True)
    finally:
        db.session.close()
