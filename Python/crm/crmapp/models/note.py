#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import datetime
from sqlalchemy import Table, Column, Boolean, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from . import Base
from .. import app


class Note(Base):
    """
    Заметки
    """
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    client_id = Column(Integer, ForeignKey('client.id'))
    title = Column(String)
    text = Column(String)
    created = Column(DateTime) # Дата создания

    # Связи
    user = relationship("User", primaryjoin="Note.user_id==User.id", uselist=False)
    client = relationship("Client", primaryjoin="Note.client_id==Client.id", uselist=False)

    def __init__(self, user, client, title):
        assert type(user).__name__=='User', app.logger.info('Не передан объект User')
        assert type(client).__name__=='Client', app.logger.info('Не передан объект Client')
        self.user_id = user.id
        self.client_id = client.id
        self.title = title
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Note %r>' % (self.title)
