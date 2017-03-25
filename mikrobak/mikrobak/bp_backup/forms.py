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
    BooleanField,
    TextField,
    TextAreaField,
    PasswordField,
    HiddenField,
    IntegerField,
    SelectField
)


class BackupDeleteForm(Form):
    pass


class BackupEditForm(Form):
    title = TextField('Название')
    backuptext = TextAreaField('Настройки')
    comment = TextAreaField('Комментарии')


class BackupUploadForm(Form):
    ip = TextField('IP', default='192.168.88.1')
    username = TextField('Логин', default='admin')
    password = PasswordField('Пароль')
