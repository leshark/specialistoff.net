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


class Client(Base):
    """
    Клиенты
    """
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    description = Column(String)
    created = Column(DateTime) # Дата создания

    # Связи
    user = relationship("User", primaryjoin="Client.user_id==User.id", uselist=False)
    contacts = relationship("Contact", primaryjoin="Client.id==Contact.client_id")
    trash = relationship("TrashClient", primaryjoin="Client.id==TrashClient.client_id", uselist=False)

    def __init__(self, user, name):
        assert type(user).__name__=='User', app.logger.info('Не передан объект User')
        self.user_id = user.id
        self.name = name
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Client %r>' % (self.name)
