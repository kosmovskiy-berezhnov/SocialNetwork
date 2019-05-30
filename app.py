import os
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


from services import notificationService
from services import content_creationService
from services import registrationService
from services import authorizationService
from services import communityService
from services import userService

app.register_blueprint(notificationService.mod)
app.register_blueprint(content_creationService.mod)
app.register_blueprint(registrationService.mod)
app.register_blueprint(authorizationService.mod)
app.register_blueprint(communityService.mod)
app.register_blueprint(userService.mod)
# db.drop_all()
# db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000, debug=True)
