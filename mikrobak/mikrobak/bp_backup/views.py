#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import (
    abort,
    render_template,
    request,
    escape,
    redirect,
    session
)

from . import bp_backup, forms
from .. import app, lib, models

@bp_backup.route('/<int:id>')
def backup_view(id):
    pagedata = {}
    pagedata['backup'] = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.id==id
    ).first()
    body = render_template('backup_view.html', pagedata=pagedata)
    return body


@bp_backup.route('/<int:id>/delete', methods=['GET', 'POST'])
def backup_delete(id):
    pagedata = {}
    pagedata['form'] = forms.BackupDeleteForm(request.form)
    pagedata['backup'] = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.id==id
    ).first()
    if not pagedata['backup']:
        abort(404)
    if request.method == 'POST':
        device = pagedata['backup'].device_id
        models.db_session.delete(pagedata['backup'])
        models.db_session.commit()
        return redirect('/device/' + str(device), code=302)
    body = render_template('backup_delete.html', pagedata=pagedata)
    return body


@bp_backup.route('/<int:id>/edit', methods=['GET', 'POST'])
def backup_edit(id):
    pagedata = {}
    pagedata['form'] = forms.BackupEditForm(request.form)
    pagedata['backup'] = models.db_session.query(
        models.Backup
    ).filter(
        models.Backup.id==id
    ).first()
    if not pagedata['backup']:
        abort(404)
    if request.method=='POST':
        pagedata['backup'].title = escape(pagedata['form'].title.data)
        pagedata['backup'].text = escape(pagedata['form'].backuptext.data)
        pagedata['backup'].comment = escape(pagedata['form'].comment.data)
        models.db_session.commit()
        return redirect('/backup/' + str(id), code=302)
    else:
        pagedata['form'] = forms.BackupEdit(request.form,
            data={'title': pagedata['backup'].title,
                'backuptext': pagedata['backup'].text,
                'comment': pagedata['backup'].comment})
    body = render_template('backupedit.html', pagedata=pagedata)
    return body


@bp_backup.route('/<int:id>/upload', methods=['GET', 'POST'])
def backup_upload(id):
    pagedata = {}
    pagedata['form'] = forms.BackupUploadForm(request.form)
    pagedata['backup'] = models.db_session.query(models.Backup).filter(models.Backup.id == id).first()
    if request.method == 'POST':
        if pagedata['backup']:
            pass
    body = render_template('upload.html', pagedata=pagedata)
    return body
