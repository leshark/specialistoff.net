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


class DeleteNoteForm(Form):
    pass


class EditNoteForm(Form):
    title = TextField('Заголовок')
    text = TextAreaField('Текст')
