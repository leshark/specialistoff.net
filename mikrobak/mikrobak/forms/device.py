#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from wtforms import Form, TextField, TextAreaField, RadioField

class DeviceNew(Form):
    devicename = TextField('Имя')
    ip = TextField('IP')
    username = TextField('Пользователь')
    password = TextField('Пароль')
    sn = TextField('Серийный номер')

class DeviceEdit(Form):
    devicename = TextField('Имя')
    ip = TextField('IP')
    username = TextField('Пользователь')
    password = TextField('Пароль')
    sn = TextField('Серийный номер')

class DeviceDelete(Form):
    pass

class BackupForm(Form):
    title = TextField('Название')
    backuptext = TextAreaField('Настройки')

class BackupEdit(Form):
    title = TextField('Название')
    backuptext = TextAreaField('Настройки')
    comment = TextAreaField('Комментарии')
