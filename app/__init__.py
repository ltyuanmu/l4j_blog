#-*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_pagedown import PageDown
#from celery import Celery, platforms
import logging
import datetime
from datetime import timedelta
import os 

basedir=os.path.abspath('.')
log_=os.path.join(basedir,'logs/l4j.us.log')
# 日志记录
logger = logging.getLogger("video4sex")
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler(log_)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)
login_manager.session_protect = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap(app)
mail = Mail(app)
pagedown = PageDown(app)
db = SQLAlchemy(app, use_native_unicode='utf8')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint,url_prefix='/auth')

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint,url_prefix='/admin')



from app import views