#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import datetime
from sqlalchemy import Table, Column, Boolean, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relationship

from . import Base


class TrashClient(Base):
    """
    Корзина для клиентов
    """
    __tablename__ = "trashclient"

    id = Column(Integer, primary_key=True)
    # ID пользователя
    user_id = Column(Integer, ForeignKey('user.id'))
    # ID книги
    client_id = Column(Integer, ForeignKey('client.id'))
    # Дата удаления
    created = Column(DateTime)

    # Связи
    user = relationship("User", primaryjoin="TrashClient.user_id==User.id")
    client = relationship("Client", primaryjoin="TrashClient.client_id==Client.id")

    def __init__(self, user, client):
        assert type(user).__name__=='User', app.logger.info('Не передан объект User')
        assert type(client).__name__=='Client', app.logger.info('Не передан объект Client')
        self.user_id = user.id
        self.client_id = client.id
        self.created = datetime.datetime.utcnow()
