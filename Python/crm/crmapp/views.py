#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import json
import os
import sys
import uuid
import random
import datetime

from flask import (
    Flask,
    session,
    render_template,
    request,
    escape,
    redirect,
    make_response,
    jsonify
)
from jinja2 import Environment, FileSystemLoader

from . import app, models, forms, lib
from .decorators import login_required


def read_json(filename):
    """
    Считываем данные в формате JSON из файла filename
    """
    result = None
    with open(filename) as json_data:
        result = json.load(json_data)
        json_data.close()
    return result


@app.route('/')
@login_required
def index():
    pagedata = {'title': '{}'.format(app.config['TITLE'])}
    pagedata['notes'] = models.db_session.query(
        models.Note
    ).order_by(
        models.Note.created.desc()
    )
    pagedata['pagination'] = lib.Pagination(
        1,
        app.config['ITEMS_ON_PAGE'],
        pagedata['notes'].count()
    )
    pagedata['notes'] = lib.getpage(pagedata['notes'], 1)
    pagedata['notes'] = pagedata['notes'].all()
    return render_template('index.html', pagedata=pagedata)


@app.route('/cabinet')
@login_required
def cabinet():
    pagedata = {'title': 'Личный кабинет - {}'.format(app.config['TITLE'])}
    pagedata['notes'] = models.db_session.query(
        models.Note
    ).filter(
        models.Note.user_id==lib.get_user().id
    ).order_by(
        models.Note.created.desc()
    ).all()
    trash = models.db_session.query(
        models.TrashClient.client_id
    )
    pagedata['clients'] = models.db_session.query(
        models.Client
    ).filter(
        ~models.Client.id.in_(trash),
        models.Client.user_id==lib.get_user().id
    ).order_by(
        models.Client.created.desc()
    ).all()
    body = render_template('cabinet.html', pagedata=pagedata)
    return body


@app.route('/clients', defaults={'page': 1})
@app.route('/clients/<int:page>')
@login_required
def clients(page):
    pagedata = {'title': 'Список клиентов - %s' % app.config['TITLE']}
    trash = models.db_session.query(
        models.TrashClient.client_id
    )
    pagedata['clients'] = models.db_session.query(
        models.Client
    ).filter(
        ~models.Client.id.in_(trash)
    ).order_by(
        models.Client.name.asc()
    )
    pagedata['pagination'] = lib.Pagination(
        page,
        app.config['ITEMS_ON_PAGE'],
        pagedata['clients'].count()
    )
    pagedata['pagination'].url = '/clients'
    pagedata['clients'] = lib.getpage(
        pagedata['clients'],
        page,
        app.config['ITEMS_ON_PAGE']
    )
    pagedata['clients'] = pagedata['clients'].all()
    return render_template('clients.html', pagedata=pagedata)


@app.route('/legal')
def legal():
    return redirect('http://specialistoff.net/legal', code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pagedata = {'title': 'Вход - ' + app.config['TITLE']}
    pagedata['form'] = forms.LoginForm(request.form)
    if request.method == 'POST':
        user = models.db_session.query(models.User).filter(
            models.User.name==escape(pagedata['form'].username.data),
            models.User.password==lib.get_hash_password(
                escape(pagedata['form'].password.data),
                app.config['SECRET_KEY']
            ),
            models.User.disable==False
        ).first()
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['ip'] = lib.get_ip()
            return redirect('/')
    pagedata['title'] = app.config['TITLE'] + ' - Вход'
    body = render_template('login.html', pagedata=pagedata)
    return body


@app.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/notes', defaults={'page': 1})
@app.route('/notes/<int:page>')
@login_required
def notes(page):
    pagedata = {'title': '{}'.format(app.config['TITLE'])}
    pagedata['notes'] = models.db_session.query(
        models.Note
    ).order_by(
        models.Note.created.desc()
    )
    pagedata['pagination'] = lib.Pagination(
        page,
        app.config['ITEMS_ON_PAGE'],
        pagedata['notes'].count()
    )
    pagedata['notes'] = lib.getpage(pagedata['notes'], page)
    pagedata['notes'] = pagedata['notes'].all()
    return render_template('notes.html', pagedata=pagedata)


@app.route('/trash', defaults={'page': 1})
@app.route('/trash/<int:page>')
@login_required
def trash(page):
    pagedata = {'title': 'Список клиентов в корзине - %s' % app.config['TITLE']}
    trash = models.db_session.query(
        models.TrashClient.client_id
    )
    pagedata['clients'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id.in_(trash)
    ).order_by(
        models.Client.name.asc()
    )
    pagedata['pagination'] = lib.Pagination(
        page,
        app.config['ITEMS_ON_PAGE'],
        pagedata['clients'].count()
    )
    pagedata['pagination'].url = '/clients'
    pagedata['clients'] = lib.getpage(
        pagedata['clients'],
        page,
        app.config['ITEMS_ON_PAGE']
    )
    pagedata['clients'] = pagedata['clients'].all()
    return render_template('trash.html', pagedata=pagedata)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def error_missing(exception):
    pagedata = {}
    error_message = "Нет ресурса. Не судьба..."
    return render_template("error.html", error_code=404, error_message=error_message, pagedata=pagedata), 404


# noinspection PyUnusedLocal
@app.errorhandler(403)
def error_unauthorized(exception):
    pagedata = {}
    error_message = "Нет прав. Не судьба..."
    return render_template("error.html", error_code=403, error_message=error_message, pagedata=pagedata), 403


# noinspection PyUnusedLocal
@app.errorhandler(500)
def error_crash(exception):
    pagedata = {}
    error_message = "Не судьба..."
    return render_template("error.html", error_code=500, error_message=error_message, pagedata=pagedata), 500


if __name__ == '__main__':
    app.run(debug=True)
