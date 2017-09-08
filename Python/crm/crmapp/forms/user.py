#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from wtforms import (
    validators,
    Form,
    TextField,
    PasswordField,
    SelectField,
    HiddenField,
    TextAreaField,
    IntegerField
)


class RegistrationForm(Form):
    username = TextField('Логин', [validators.Length(min=4, max=25)])
    email = TextField('E-mail', [validators.Length(min=6, max=35)])
    humpass = HiddenField()


class LoginForm(Form):
    username = TextField('Логин', [validators.Length(min=4, max=25)])
    password = PasswordField('Пароль', [validators.DataRequired()])


class ForgotForm(Form):
    email = TextField('Выслать пароль на e-mail')
    humpass = HiddenField()
