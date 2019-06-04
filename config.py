from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)
url_address = '127.0.0.1'
app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secretkey',
                  USERNAME='admin', PASSWORD='admin')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/socialNetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

