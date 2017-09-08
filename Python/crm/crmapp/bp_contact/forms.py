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


class EditContactForm(Form):
    contact_value = TextField('Значение')
    contact_type = SelectField(
        'Тип контакта',
        choices=[
            ('phone', 'Телефон'),
            ('url', 'Веб-сайт'),
            ('telegram', 'Telegram'),
            ('icq', 'ICQ'),
            ('xmpp', 'Jabber/XMPP'),
            ('skype', 'Skype'),
            ('email', 'E-mail')
        ]
    )


class DeleteContactForm(Form):
    pass
