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
from flask import Flask, render_template, request, escape, redirect, jsonify
from models import *
import forms

from difflib import Differ

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    body = render_template('index.html')
    return body

@app.route('/devices', methods=['GET'])
def devices():
    pagedata = {}
    pagedata['devices'] = db_session.query(Device).order_by(Device.name).all()
    body = render_template('devices.html', pagedata=pagedata)
    return body

@app.route('/device/add', methods=['GET', 'POST'])
def deviceadd():
    pagedata = {}
    pagedata['form'] = forms.DeviceNew(request.form)
    if request.method == 'POST':
        newdev = Device(name=escape(pagedata['form'].devicename.data),
            ip=escape(pagedata['form'].ip.data),
            username=escape(pagedata['form'].username.data),
            password=escape(pagedata['form'].password.data))
        if 'sn' in request.form.keys():
            newdev.serialnumber = escape(pagedata['form'].sn.data)
        db_session.add(newdev)
        db_session.commit()
        return redirect('/devices', code=302)
    body = render_template('deviceadd.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/edit', methods=['GET', 'POST'])
def deviceedit(id):
    pagedata = {}
    pagedata['form'] = forms.DeviceEdit(request.form)
    pagedata['device'] = db_session.query(Device).filter(Device.id == id).first()
    if request.method == 'POST':
        if pagedata['device']:
            pagedata['device'].name = escape(pagedata['form'].devicename.data)
            pagedata['device'].ip = escape(pagedata['form'].ip.data)
            pagedata['device'].username = escape(pagedata['form'].username.data)
            pagedata['device'].password = escape(pagedata['form'].password.data)
        db_session.commit()
    else:
        if pagedata['device']:
            pagedata['form'].devicename.data = pagedata['device'].name
            pagedata['form'].ip.data = pagedata['device'].ip
            pagedata['form'].username.data = pagedata['device'].username
            pagedata['form'].password.data = pagedata['device'].password
            pagedata['form'].sn.data = pagedata['device'].serialnumber
    body = render_template('deviceedit.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/delete', methods=['GET', 'POST'])
def devicedelete(id):
    pagedata = {}
    pagedata['form'] = forms.DeviceDelete(request.form)
    pagedata['device'] = db_session.query(Device).filter(Device.id == id).first()
    if request.method == 'POST':
        if pagedata['device']:
            if pagedata['form'].delete.data == 'yes':
                db_session.delete(pagedata['device'])
                db_session.commit()
        return redirect('/devices', code=302)
    body = render_template('devicedeleteconfirm.html', pagedata=pagedata)
    return body

@app.route('/device/', defaults={'id': 0})
@app.route('/device/<int:id>')
def device(id):
    pagedata = {}
    pagedata['device'] = db_session.query(Device).filter(Device.id == id).first()
    if pagedata['device']:
        pagedata['backups'] = db_session.query(Backup).filter(Backup.device_id == id).all()
    body = render_template('device.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/backup')
def backup(id):
    pagedata = {}
    pagedata['device'] = db_session.query(Device).filter(Device.id == id).first()
    body = render_template('backup.html', pagedata=pagedata)
    return body

@app.route('/device/<int:id>/backupdl', methods=['POST'])
def getbackup(id):
    pagedata = {}
    pagedata['device'] = db_session.query(Device).filter(Device.id == id).first()
    sshCli = SSHClient()
    sshCli.set_missing_host_key_policy(AutoAddPolicy())
    print(pagedata['device'].ip)
    sshCli.connect(pagedata['device'].ip,
        port=22,
        username=pagedata['device'].username,
        password=pagedata['device'].password,
        look_for_keys=False)
    stdin, stdout, stderr = sshCli.exec_command('/export')
    time.sleep(15)
    sshCli.close()
    pagedata['settings'] = stdout.read().decode('utf-8')
    pagedata['error'] = stderr.read().decode('utf-8')
    body = jsonify({'settings': pagedata['settings'],
        'error': pagedata['error']})
    return body

@app.route('/device/<int:id>/save', methods=['POST'])
def save(id):
    device = db_session.query(Device).filter(Device.id == id).first()
    backup = Backup(device_id=id,
        title=escape(request.form['title']),
        text=escape(request.form['backuptext']))
    db_session.add(backup)
    db_session.commit()
    return redirect('/device/'+str(id), code=302)

@app.route('/backup/<int:id>')
def backupview(id):
    pagedata = {}
    pagedata['backup'] = db_session.query(Backup).filter(Backup.id == id).first()
    body = render_template('backupview.html', pagedata=pagedata)
    return body
    
@app.route('/diff', methods=['POST'])
def diffbackup():
    pagedata = {}
    baklist = request.form.getlist('backup')
    d = Differ()
    text1 = db_session.query(Backup).filter(Backup.id == baklist[0]).first()
    text2 = db_session.query(Backup).filter(Backup.id == baklist[1]).first()
    pagedata['backups'] = [text1, text2]
    pagedata['diff'] = '\n'.join(list(d.compare(text1.text.split("\n"), text2.text.split("\n"))))
    body = render_template('diffview.html', pagedata=pagedata)
    return body
