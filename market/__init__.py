from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flaskmarket'
app.config['SECRET_KEY']='b80e37fd7a7703389baef731'
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
import market.models as models
import market.routes as routes


