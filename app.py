import os
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, json
# from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRS, SAFRSAPI, SAFRSBase
from models.swagger_init import expose
from config import app

url_address = '127.0.0.1'
api = SAFRSAPI(app, host=url_address, port=5000, prefix='/api/docs')
app.app_context().push()
expose(api)


@app.route('/')
def home():
    return render_template('home.html')


from services import notificationService
from services import content_creationService
from services import registrationService
from services import authorizationService
from services import communityService

# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(notificationService.mod)
app.register_blueprint(content_creationService.mod)
app.register_blueprint(registrationService.mod)
app.register_blueprint(authorizationService.mod)
app.register_blueprint(communityService.mod)


if __name__ == '__main__':
    app.debug = True
    app.run(host=url_address, port=5000, debug=True)
