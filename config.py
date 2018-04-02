#-*- coding=utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SSDFDSFDFD'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:NewtouchOne123@183.66.65.246:30796/blog'
#SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True
