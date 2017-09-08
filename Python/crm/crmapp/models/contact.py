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


class Contact(Base):
    """
    Контакты клиентов
    """
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    contact_type = Column(String)
    contact_value = Column(String)
    created = Column(DateTime) # Дата создания

    # Связи
    client = relationship("Client", primaryjoin="Contact.client_id==Client.id", uselist=False)

    def __init__(self, client, contact_type, contact_value):
        assert type(client).__name__=='Client', app.logger.info('Не передан объект Client')
        self.client_id = client.id
        self.contact_type = contact_type
        self.contact_value = contact_value
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Contact {}>'.format(self.name)
