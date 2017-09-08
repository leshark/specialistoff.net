#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import datetime

from flask import session, redirect
from functools import wraps

from . import models

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and 'user_id' in session:
            user = models.db_session.query(
                models.User
            ).filter(
                models.User.id==session['user_id']
            ).first()
            if user:
                user.last_activity = datetime.datetime.utcnow()
                models.db_session.commit()
                return func(*args, **kwargs)
            else:
                session.pop('logged_in', None)
                session.pop('user_id', None)
                return redirect('/login')
        else:
            return redirect('/login')
    return decorated_function
