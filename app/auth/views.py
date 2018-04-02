#-*- coding=utf-8 -*-
import datetime
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import *
from .forms import *
from .. import logger

# AUTH


@auth.before_request
def before_request():
    global ip
    try:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    except:
        ip = request.remote_addr


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            session['logged_in'] = True
            session['admin'] = False
            if user.id == 1:
                session['admin'] = True
            session.permanent = True
            #print(u'登陆成功')
            return redirect('/')
        else:
            #print(u'邮箱或密码错误')
            return redirect('/')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    session.pop('admin', None)
    #print(u'你已经注销！')
    return redirect('/')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(email=email, username=username,password=password)
        db.session.add(user)
        db.session.commit()
        #print(u'注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            print(u'修改密码成功！')
            return redirect(url_for('online.index'))
        else:
            print(u'无效密码')
            return redirect(url_for('auth.change_password'))
    return render_template("admin/change_password.html", form=form)

