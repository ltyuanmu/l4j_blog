#-*- coding=utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User
from flask import session


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=True)
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    username = StringField('username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名由字母、数字、下划线组成')])
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='password must be same')])
    password2 = PasswordField('re-password', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email has been register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username has been register')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old password', validators=[DataRequired()])
    password = PasswordField('newpassword', validators=[
        DataRequired(), EqualTo('password2', message='password must be same')])
    password2 = PasswordField('re-password', validators=[DataRequired()])
    submit = SubmitField('Update Password')
