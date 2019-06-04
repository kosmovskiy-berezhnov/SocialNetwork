from flask import g
from flask_login import current_user, LoginManager
from safrs import SAFRSAPI

from config import app, db, url_address
from models.administrator import Administrator
from models.swagger_init import expose
from models.user import User

lm = LoginManager()
lm.init_app(app=app)
lm.login_view = 'authorization.login'


@lm.user_loader
def get_user(ident):
    from models.user import User
    return User.query.get(int(ident))


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()


@app.before_request
def before_request():
    g.user = current_user
    g.id = 0 if not g.user.is_authenticated else g.user.id


api = SAFRSAPI(app, host=url_address, port=5000, prefix='/api/docs')
app.app_context().push()
expose(api)

# @app.after_request
# def after_request(response):
#     db.session.close()
#     return response


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
        app.run(host=url_address, port=5000)
    finally:
        db.session.close()
