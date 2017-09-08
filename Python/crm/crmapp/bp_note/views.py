#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import render_template, request, abort, escape, redirect, session

from . import bp_note, forms
from .. import app, lib, models
from ..decorators import login_required


@login_required
@bp_note.route('/<int:id>')
def note_id(id):
    pagedata = {'title': 'Заметка по клиенту - {}'.format(app.config['TITLE'])}
    pagedata['note'] = models.db_session.query(
        models.Note
    ).filter(
        models.Note.id==id
    ).first()
    if not pagedata['note']:
        abort(404)
    body = render_template('note.html', pagedata=pagedata)
    return body


@bp_note.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def note_delete(id):
    pagedata = {}
    pagedata['title'] = 'Удалить заметку - {}'.format(app.config['TITLE'])
    pagedata['note'] = models.db_session.query(
        models.Note
    ).filter(
        models.Note.id==id
    ).first()
    if not pagedata['note']:
        abort(404)
    pagedata['form'] = forms.DeleteNoteForm(request.form)
    if request.method=='POST':
        if pagedata['form'].validate:
            client_id = pagedata['note'].client.id
            models.db_session.delete(pagedata['note'])
            models.db_session.commit()
            return redirect('/client/{}'.format(client_id), code=302)
    body = render_template('note_delete.html', pagedata=pagedata)
    return body


@bp_note.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def note_edit(id):
    pagedata = {}
    pagedata['title'] = 'Редактирование клиента - {}'.format(app.config['TITLE'])
    pagedata['note'] = models.db_session.query(
        models.Note
    ).filter(
        models.Note.id==id
    ).first()
    if not pagedata['note']:
        abort(404)
    pagedata['form'] = forms.EditNoteForm(
        request.form,
        data={
            'title': pagedata['note'].title,
            'text': pagedata['note'].text
        }
    )
    if request.method=='POST':
        if pagedata['form'].validate:
            pagedata['note'].title = pagedata['form'].title.data
            pagedata['note'].text = pagedata['form'].text.data
            models.db_session.commit()
            return redirect('/note/{}'.format(id), code=302)
    body = render_template('note_edit.html', pagedata=pagedata)
    return body
