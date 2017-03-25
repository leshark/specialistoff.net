#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import config
import logging

from flask import Flask
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config.CONFIG)

# Логирование
handler = RotatingFileHandler(app.config['LOG_FILE'],
                              maxBytes=app.config['LOG_FILE_SIZE'] * 1024 * 1024,
                              backupCount=1)

handler.setLevel(logging.INFO)
formatter = logging.Formatter(app.config['LONG_LOG_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# celery
from celery import Celery

celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'],
                include=['mikrobak.tasks'])
celery.conf.update(app.config)

from .bp_backup import bp_backup as backup_blueprint
app.register_blueprint(backup_blueprint, url_prefix='/backup')

import mikrobak.views
