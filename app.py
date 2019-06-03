import os
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, json
# from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRS, SAFRSAPI, SAFRSBase
from models.swagger_init import expose
from config import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, LoginManager


lm = LoginManager()
lm.init_app(app=app)
lm.login_view = 'login'


@lm.user_loader
def get_user(ident):
    from models.user import User
    return User.query.get(int(ident))


@app.before_request
def before_request():
    g.user = current_user
    g.id = 0 if not g.user.is_authenticated else g.user.id


url_address = '127.0.0.1'
api = SAFRSAPI(app, host=url_address, port=5000, prefix='/api/docs')
app.app_context().push()
expose(api)


from services import notificationService
from services import content_creationService
from services import registrationService
from services import authorizationService
from services import communityService
from services import userService
from services import adminService

app.register_blueprint(notificationService.mod)
app.register_blueprint(content_creationService.mod)
app.register_blueprint(registrationService.mod)
app.register_blueprint(authorizationService.mod)
app.register_blueprint(communityService.mod)
app.register_blueprint(userService.mod)
app.register_blueprint(adminService.mod)
# db.drop_all()
# db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
