# -*- coding=utf-8 -*-
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True), 'Moderator': (Permission.FOLLOW |
                                                                     Permission.COMMENT |
                                                                     Permission.WRITE_ARTICLES |
                                                                     Permission.MODERATE_COMMENTS, False), 'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(permissions=0xff).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def vip_(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Post(db.Model):
    __tablename__='posts'
    pid=db.Column(db.Integer,primary_key=True) #文章id，自增
    title=db.Column(db.String(255),index=True)
    context=db.Column(db.Text(100000))
    description=db.Column(db.String(255))
    inserttime=db.Column(db.String(64),default=datetime.datetime.now().strftime('%Y-%m%d %H:%M:%S'))
    source=db.Column(db.String(32),index=True,unique=True)
    source_url=db.Column(db.String(255),index=True)
    viewtimes=db.Column(db.Integer,default=0)

    @staticmethod
    def add_views(pid):
        post=Post.query.filter_by(pid=pid).first()
        post.viewtimes+=1
        db.session.add(post)
        db.session.commit()


