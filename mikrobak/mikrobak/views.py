#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

import time
import datetime

from paramiko import SSHClient
from paramiko import AutoAddPolicy

from mikrobak import app
from flask import (
    Flask,
    render_template,
    request,
    escape,
    redirect,
    jsonify,
    abort
)

# RemiZOffAlex
from . import lib, models, forms
import difflib


"""
Постраничный вывод
"""
def getpage(query, page=1, page_size=10):
    if page_size:
        query = query.limit(page_size)
    if page:
        query = query.offset((page-1)*page_size)
    return query


@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    pagedata = {}
    pagedata['title'] = "Главная страница"
    body = render_template('index.html', pagedata=pagedata)
    return body


@app.route('/backups', defaults={'page': 1})
@app.route('/backups/<int:page>')
def backups(page):
    pagedata = {}
    pagedata['backups'] = models.db_session.query(models.Backup).order_by(models.Backup.created.desc())
    pagedata['pagination'] = lib.Pagination(
        page,
        10,
        pagedata['backups'].count())
    pagedata['backups'] = getpage(pagedata['backups'], page)
    pagedata['backups'] = pagedata['backups'].all()
    body = render_template('backups.html', pagedata=pagedata)
    return body


@app.route('/devices', methods=['GET'])
def devices():
    pagedata = {}
    pagedata['title'] = "Список устройств"
    pagedata['devices'] = models.db_session.query(
        models.Device
    ).order_by(
        models.Device.name
    ).all()
    body = render_template('devices.html', pagedata=pagedata)
    return body

@app.route('/device/add', methods=['GET', 'POST'])
def deviceadd():
    pagedata = {}
    pagedata['title'] = "Добавление нового устройства"
    pagedata['form'] = forms.DeviceNew(request.form)
    if request.method == 'POST':
        newdev = models.Device(name=escape(pagedata['form'].devicename.data),
            ip=escape(pagedata['form'].ip.data),
            username=escape(pagedata['form'].username.data),
            password=escape(pagedata['form'].password.data))
        if 'sn' in request.form.keys():
            newdev.serialnumber = escape(pagedata['form'].sn.data)
        models.db_session.add(newdev)
        models.db_session.commit()
        return redirect('/devices', code=302)
    body = render_template('deviceadd.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/edit', methods=['GET', 'POST'])
def deviceedit(id):
    pagedata = {}
    pagedata['form'] = forms.DeviceEdit(request.form)
    pagedata['device'] = models.db_session.query(models.Device).filter(models.Device.id == id).first()
    if not pagedata['device']:
        abort(404)
    if request.method == 'POST':
        pagedata['device'].name = escape(pagedata['form'].devicename.data)
        pagedata['device'].ip = escape(pagedata['form'].ip.data)
        pagedata['device'].username = escape(pagedata['form'].username.data)
        pagedata['device'].password = escape(pagedata['form'].password.data)
        models.db_session.commit()
        return redirect('/devices', code=302)
    else:
        pagedata['form'] = forms.DeviceEdit(request.form,
            data={'devicename': pagedata['device'].name,
                'ip': pagedata['device'].ip,
                'username': pagedata['device'].username,
                'password': pagedata['device'].password,
                'sn': pagedata['device'].serialnumber})
    body = render_template('device_edit.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/delete', methods=['GET', 'POST'])
def devicedelete(id):
    pagedata = {}
    pagedata['form'] = forms.DeviceDelete(request.form)
    pagedata['device'] = models.db_session.query(
        models.Device
    ).filter(
        models.Device.id==id
    ).first()
    if not pagedata['device']:
        abort(404)
    if request.method == 'POST':
        for item in pagedata['device'].backups:
            models.db_session.delete(item)
        models.db_session.delete(pagedata['device'])
        models.db_session.commit()
        return redirect('/devices', code=302)
    body = render_template('device_delete.html', pagedata=pagedata)
    return body


@app.route('/device/', defaults={'id': 0})
@app.route('/device/<int:id>')
def device(id):
    pagedata = {}
    pagedata['device'] = models.db_session.query(
        models.Device
    ).filter(
        models.Device.id==id
    ).first()
    if not pagedata['device']:
        abort(404)
    pagedata['backups'] = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.device_id==id
    ).all()
    body = render_template('device.html', pagedata=pagedata)
    return body


@app.route('/device/<int:id>/backup')
def backup(id):
    pagedata = {}
    pagedata['form'] = forms.BackupForm(request.form)
    pagedata['device'] = models.db_session.query(models.Device).filter(models.Device.id == id).first()
    body = render_template('backup.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/backupdl', methods=['POST'])
def getbackup(id):
    pagedata = {}
    pagedata['device'] = models.db_session.query(models.Device).filter(models.Device.id == id).first()
    sshCli = SSHClient()
    sshCli.set_missing_host_key_policy(AutoAddPolicy())
    print(pagedata['device'].ip)
    sshCli.connect(pagedata['device'].ip,
        port=22,
        username=pagedata['device'].username,
        password=pagedata['device'].password,
        look_for_keys=False)
    stdin, stdout, stderr = sshCli.exec_command('/export')
    time.sleep(25)
    sshCli.close()
    pagedata['settings'] = stdout.read().decode('utf-8')
    pagedata['error'] = stderr.read().decode('utf-8')
    body = jsonify({'settings': pagedata['settings'],
        'error': pagedata['error']})
    return body

@app.route('/device/<int:id>/save', methods=['POST'])
def save(id):
    pagedata = {}
    pagedata['form'] = forms.BackupForm(request.form)
    device = models.db_session.query(models.Device).filter(models.Device.id == id).first()
    backup = models.Backup(device_id=id,
        title=escape(request.form['title']),
        text=escape(request.form['backuptext']))
    models.db_session.add(backup)
    models.db_session.commit()
    return redirect('/device/'+str(id), code=302)


@app.route('/diff', methods=['POST'])
def diffbackup():
    pagedata = {}
    baklist = request.form.getlist('backup')
    text1 = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.id==baklist[0]
    ).first()
    text2 = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.id==baklist[1]
    ).first()
    pagedata['backups'] = [text1, text2]
    pagedata['diff'] = '\n'.join(list(difflib.unified_diff(text1.text.split("\n"), text2.text.split("\n"))))
    body = render_template('diffview.html', pagedata=pagedata)
    return body


# noinspection PyUnusedLocal
@app.errorhandler(404)
def error_missing(exception):
    pagedata = {}
    error_message = "Не судьба..."
    return render_template("error.html", error_code=404, error_message=error_message, pagedata=pagedata), 404


# noinspection PyUnusedLocal
@app.errorhandler(403)
def error_unauthorized(exception):
    pagedata = {}
    error_message = "You are not authorized to view this page. Ensure you have the correct permissions."
    return render_template("error.html", error_code=403, error_message=error_message, pagedata=pagedata), 403


# noinspection PyUnusedLocal
@app.errorhandler(500)
def error_crash(exception):
    pagedata = {}
    error_message = "Вот незадача..."
    return render_template("error.html", error_code=500, error_message=error_message, pagedata=pagedata), 500
