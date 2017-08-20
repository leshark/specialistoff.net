#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from myapp import app
from flask import Flask, render_template, request

from . import forms, models

@app.route('/', methods=['GET'])
def index():
    pagedata = {}
    pagedata['title'] = app.config['TITLE']
    pagedata['info'] = 'Привет мир!'
    body = render_template('index.html', pagedata=pagedata)
    return body

@app.route('/login', methods=['GET', 'POST'])
def login():
    pagedata = {}
    pagedata['form'] = forms.LoginForm(request.form)
    body = render_template('login.html', pagedata=pagedata)
    return body
