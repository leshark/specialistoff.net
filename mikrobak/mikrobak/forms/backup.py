#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from wtforms import Form, TextField, TextAreaField, RadioField, PasswordField


class Backup(Form):
    title = TextField('Название')
    backuptext = TextAreaField('Настройки')


class BackupEdit(Form):
    title = TextField('Название')
    backuptext = TextAreaField('Настройки')
    comment = TextAreaField('Комментарии')

class BackupUpload(Form):
    ip = TextField('IP', default='192.168.88.1')
    username = TextField('Логин', default='admin')
    password = PasswordField('Пароль')