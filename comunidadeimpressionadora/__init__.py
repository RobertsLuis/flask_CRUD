#PACKAGE TO IMPORT EVERYTHING EVERY TIME WE RUN THE APP

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '6136075b5881ebfe576b1e12a64afa12'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Faça login para acessar a página"
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import pages
