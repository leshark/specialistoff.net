#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import render_template, request, abort, escape, redirect, session

from . import bp_client, forms
from .. import app, lib, models
from ..decorators import login_required


@bp_client.route('/<int:id>')
@login_required
def client_id(id):
    pagedata = {'title': 'Карточка клиента - {}'.format(app.config['TITLE'])}
    pagedata['client'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id==id
    ).first()
    if not pagedata['client']:
        abort(404)
    pagedata['notes'] = models.db_session.query(
        models.Note
    ).filter(
        models.Note.client_id==id
    )
    pagedata['pagination'] = lib.Pagination(
        1,
        4,
        pagedata['notes'].count())
    pagedata['notes'] = lib.getpage(pagedata['notes'], 1)
    pagedata['notes'] = pagedata['notes'].all()
    body = render_template('client.html', pagedata=pagedata)
    return body


@bp_client.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def client_edit(id):
    pagedata = {}
    pagedata['title'] = 'Редактирование клиента - {}'.format(app.config['TITLE'])
    pagedata['client'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id==id
    ).first()
    if not pagedata['client']:
        abort(404)
    pagedata['form'] = forms.EditClientForm(
        request.form,
        data={
            'name': pagedata['client'].name,
            'description': pagedata['client'].description
        }
    )
    if request.method=='POST':
        if pagedata['form'].validate:
            pagedata['client'].name = pagedata['form'].name.data
            pagedata['client'].description = pagedata['form'].description.data
            models.db_session.commit()
            return redirect('/client/{}'.format(pagedata['client'].id), code=302)
    body = render_template('client_edit.html', pagedata=pagedata)
    return body


@bp_client.route('/<int:id>/contactadd', methods=['GET', 'POST'])
@login_required
def client_contactadd(id):
    pagedata = {}
    pagedata['title'] = 'Добавить контакт для клиента - {}'.format(app.config['TITLE'])
    pagedata['client'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id==id
    ).first()
    if not pagedata['client']:
        abort(404)
    pagedata['form'] = forms.NewContactForm(request.form)
    if request.method=='POST':
        if pagedata['form'].validate:
            newcontact = models.Contact(
                pagedata['client'],
                pagedata['form'].contact_type.data,
                pagedata['form'].contact_value.data
            )
            models.db_session.add(newcontact)
            models.db_session.commit()
            return redirect('/client/{}'.format(pagedata['client'].id), code=302)
    body = render_template('client_contact_new.html', pagedata=pagedata)
    return body


@bp_client.route('/<int:id>/noteadd', methods=['GET', 'POST'])
@login_required
def client_noteadd(id):
    pagedata = {}
    pagedata['title'] = 'Добавить контакт для клиента - {}'.format(app.config['TITLE'])
    pagedata['client'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id==id
    ).first()
    if not pagedata['client']:
        abort(404)
    pagedata['form'] = forms.NewNoteForm(request.form)
    if request.method=='POST':
        if pagedata['form'].validate:
            newnote = models.Note(
                lib.get_user(),
                pagedata['client'],
                pagedata['form'].title.data
            )
            newnote.text = pagedata['form'].text.data
            models.db_session.add(newnote)
            models.db_session.commit()
            return redirect('/client/{}'.format(id), code=302)
    body = render_template('note_add.html', pagedata=pagedata)
    return body


@bp_client.route('/<int:id>/recovery', methods=['GET', 'POST'])
@login_required
def client_recovery(id):
    exists = models.db_session.query(
        models.TrashClient
    ).filter(
        models.TrashClient.client_id==id
    ).first()
    if exists:
        models.db_session.delete(exists)
        models.db_session.commit()
        return redirect('/client/{}'.format(exists.client_id), code=302)
    return redirect('/clients', code=302)


@bp_client.route('/<int:id>/trash', methods=['GET', 'POST'])
@login_required
def client_trash(id):
    pagedata = {}
    pagedata['title'] = 'Удаление клиента в козину - {}'.format(app.config['TITLE'])
    pagedata['client'] = models.db_session.query(
        models.Client
    ).filter(
        models.Client.id==id
    ).first()
    if not pagedata['client']:
        abort(404)
    exists = models.db_session.query(
        models.TrashClient
    ).filter(
        models.TrashClient.client_id==id
    ).first()
    if exists:
        return redirect('/clients', code=302)
    pagedata['form'] = forms.TrashClientForm(request.form)
    if request.method=='POST':
        if pagedata['form'].validate:
            new_crumple = models.TrashClient(
                lib.get_user(),
                pagedata['client']
            )
            models.db_session.add(new_crumple)
            models.db_session.commit()
            return redirect('/clients', code=302)
    body = render_template('client_trash.html', pagedata=pagedata)
    return body


@bp_client.route('/add', methods=['GET', 'POST'])
@login_required
def client_add():
    pagedata = {'title': 'Добавить клиента - ' + app.config['TITLE']}
    pagedata['form'] = forms.NewClientForm(request.form)
    if request.method == 'POST':
        if pagedata['form'].validate():
            newclient = models.Client(
                lib.get_user(),
                pagedata['form'].name.data
            )
            newclient.description = pagedata['form'].description.data
            models.db_session.add(newclient)
            models.db_session.commit()
            return redirect('/client/%s' % (str(newclient.id)))
    body = render_template('client_add.html', pagedata=pagedata)
    return body
