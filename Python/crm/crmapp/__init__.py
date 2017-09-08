#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

import config
import logging

from flask import Flask
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config.CONFIG)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Логирование
handler = RotatingFileHandler(
    app.config['LOG_FILE'],
    maxBytes=app.config['LOG_FILE_SIZE']*1024*1024,
    backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(app.config['LONG_LOG_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)


@app.context_processor
def inject_user():
    if lib.get_user():
        return dict(user=lib.get_user().name)
    return dict()

from .bp_client import bp_client as client_blueprint
app.register_blueprint(client_blueprint, url_prefix='/client')

from .bp_contact import bp_contact as contact_blueprint
app.register_blueprint(contact_blueprint, url_prefix='/contact')

from .bp_note import bp_note as note_blueprint
app.register_blueprint(note_blueprint, url_prefix='/note')

from . import views
