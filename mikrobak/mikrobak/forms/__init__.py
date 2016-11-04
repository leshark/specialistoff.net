#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

from forms.device import DeviceNew, DeviceEdit, DeviceDelete
from forms.backup import Backup, BackupEdit, BackupUpload
__all__ = [
    'DeviceNew', 'DeviceEdit', 'DeviceDelete',
    'Backup', 'BackupEdit', 'BackupUpload'
]
