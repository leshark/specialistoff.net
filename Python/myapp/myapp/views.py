#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from myapp import app
from flask import Flask, render_template

@app.route('/', methods=['GET'])
def index():
    pagedata = {}
    pagedata['info'] = 'Привет мир!'
    body = render_template('index.html', pagedata=pagedata)
    return body
