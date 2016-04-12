#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

'''
Генератор команд для MikroTik
Для тех, у кого много VLAN + нарезка скорости 3М

Пример применения шаблонов
'''

import os
import sys

from jinja2 import Template

templates = """/interface vlan
add interface=bridge-local name=vlan{{ item['id'] }} vlan-id={{ item['id'] }}
/ip address
add interface=vlan{{ item['id'] }} address={{ item['ip'] }}/24
/queue simple
add max-limit=3M/3M name=queue{{ item['id'] }} target=vlan{{ item['id'] }}

"""

vlans = [{'id': 70, 'ip': '192.168.0.2'},
{'id': 80, 'ip': '192.168.0.3'}]

for item in vlans:
    template=Template(templates)
    template=template.render(item=item)
    print(template)
