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

class User(Base):
    """
    Пользователь
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String)
    created = Column(DateTime) # Дата создания
    last_activity = Column(DateTime) # Дата последней активности
    disable = Column(Boolean)

    # Связи
    # answers = relationship("Answer", primaryjoin="User.id==Answer.user_id")

    def __init__(self, name):
        self.name = name
        self.created = datetime.datetime.utcnow()
        self.disable = False

    @property
    def days_ago(self):
        """Возвращает количество прошедших дней с последнего входа пользователя"""
        if self.last_activity:
            result = (datetime.datetime.utcnow() - self.last_activity).days
            if result < 1:
                return 'сегодня'
            elif result >= 1 and result < 2:
                return 'вчера'
            elif result >= 2 and result < 3:
                return 'позавчера'
            elif result % 10 == 1 and result % 100 != 11:
                return str(result) + ' день назад'
            elif result % 10 in [2, 3, 4] and result % 100 not in [12, 13, 14]:
                return str(result) + ' дня назад'
            elif result % 10 == 0 or result % 10 in [5, 6, 7, 8, 9] or result % 100 in [11, 12, 13, 14]:
                return str(result) + ' дней назад'
            return result
        else:
            return 'никогда'

    def __repr__(self):
        return '<User %r>' % (self.name)
