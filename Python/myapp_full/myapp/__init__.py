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

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Логирование
handler = RotatingFileHandler(app.config['LOG_FILE'],
    maxBytes=app.config['LOG_FILE_SIZE']*1024*1024,
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
    include=['myapp.tasks'])
celery.conf.update(app.config)

import views
