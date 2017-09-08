#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from wtforms import validators, Form, TextField, PasswordField, SelectField, HiddenField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class SearchForm(Form):
    search = TextField('Поиск', validators=[DataRequired()])
