from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import  os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'enter your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#sql alchemy instance
db = SQLAlchemy(app)
#bcrypt instance
bcrypt = Bcrypt(app)
#login manager instance in order to use it on our application
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes