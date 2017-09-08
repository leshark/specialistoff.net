#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from flask import render_template, request, abort, escape, redirect, session

from . import bp_contact, forms
from .. import app, lib, models
from ..decorators import login_required

@bp_contact.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def contact_edit(id):
    pagedata = {}
    pagedata['title'] = 'Редактирование контакта - {}'.format(app.config['TITLE'])
    pagedata['contact'] = models.db_session.query(
        models.Contact
    ).filter(
        models.Contact.id==id
    ).first()
    if not pagedata['contact']:
        abort(404)
    pagedata['form'] = forms.EditContactForm(
        request.form,
        data={
            'contact_value': pagedata['contact'].contact_value,
            'contact_type': pagedata['contact'].contact_type
        }
    )
    if request.method=='POST':
        if pagedata['form'].validate:
            pagedata['contact'].contact_value = pagedata['form'].contact_value.data
            pagedata['contact'].contact_type = pagedata['form'].contact_type.data
            models.db_session.commit()
            return redirect('/client/{}'.format(pagedata['contact'].client.id), code=302)
    body = render_template('contact_edit.html', pagedata=pagedata)
    return body


@bp_contact.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def contact_delete(id):
    pagedata = {}
    pagedata['title'] = 'Удалить контакт - {}'.format(app.config['TITLE'])
    pagedata['contact'] = models.db_session.query(
        models.Contact
    ).filter(
        models.Contact.id==id
    ).first()
    if not pagedata['contact']:
        abort(404)
    pagedata['form'] = forms.DeleteContactForm(request.form)
    if request.method=='POST':
        if pagedata['form'].validate:
            client_id = pagedata['contact'].client.id
            models.db_session.delete(pagedata['contact'])
            models.db_session.commit()
            return redirect('/client/{}'.format(client_id), code=302)
    body = render_template('contact_delete.html', pagedata=pagedata)
    return body
