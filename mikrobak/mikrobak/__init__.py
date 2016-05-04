#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask

app = Flask(__name__)
app.debug = True

dbpath = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbpath + '/data/mikrobak.db'

import views
