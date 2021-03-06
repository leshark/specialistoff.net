#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from wtforms import Form, BooleanField, TextField, PasswordField

class LoginForm(Form):
    username = TextField('Имя пользователя')
    password = PasswordField('Пароль')
