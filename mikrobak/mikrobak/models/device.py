#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

import datetime
from sqlalchemy import Table, Column, Boolean, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    serialnumber = Column(String)
    created = Column(DateTime)

    # Связи
    backups = relationship("Backup", backref='backup', primaryjoin="Device.id==Backup.device_id")

    def __init__(self, name, ip, username, password):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.created = datetime.datetime.utcnow()

class Backup(Base):
    __tablename__ = "backup"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    comment = Column(String)
    created = Column(DateTime)

    # Связи
    device = relationship("Device", backref='device', primaryjoin="Device.id==Backup.device_id")

    def __init__(self, device_id, title, text):
        self.device_id = device_id
        self.title = title
        self.text = text
        self.created = datetime.datetime.utcnow()
