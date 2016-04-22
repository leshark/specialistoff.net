#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

'''
Генератор команд для MikroTik
Для тех, у кого много VLAN + нарезка скорости 3М + DHCP сервер для каждого VLAN + NAT

Пример применения шаблонов
'''

import os
import sys

from jinja2 import Template
# http://ipcalc.readthedocs.org/en/latest/
import ipcalc

templates = """# Создание и настройка интерфейса
/interface vlan
add interface=bridge-local name=vlan{{ data['id'] }} vlan-id={{ data['id'] }}
/ip address
add interface=vlan{{ data['id'] }} address={{ data['net'].FirstIP }}/{{ data['net'].Bitmask }}

# Шейпер
/queue simple
add max-limit=3M/3M name=queue{{ data['id'] }} target=vlan{{ data['id'] }}

# DHCP
/ip pool
add name=pool2 ranges={{ data['net'][2] }}-{{ data['net'].LastIP }}
/ip dhcp-server
add address-pool=pool1 interface=bridge-local name=server1
/ip dhcp-server network
add address={{ data['net'].Network }}/{{ data['net'].Bitmask }} dns-server=77.88.8.8,77.88.8.1 gateway={{ data['net'].FirstIP }} netmask={{ data['net'].Bitmask }}

# NAT
/ip firewall address-list
add address={{ data['net'].Address }}/{{ data['net'].Bitmask }} list=vlans

/ip firewall nat
add action=src-nat chain=srcnat out-interface=WAN src-address-list=vlans to-addresses=XXX.XXX.XXX.XXX
# XXX.XXX.XXX.XXX - внешний IP
"""

vlans = [{'id': 10, 'ip': '10.0.1.0/29'},
{'id': 11, 'ip': '10.0.1.8/29'},
{'id': 12, 'ip': '10.0.1.16/29'},
{'id': 13, 'ip': '10.0.1.24/29'},
{'id': 14, 'ip': '10.0.1.32/29'},
{'id': 15, 'ip': '10.0.1.40/29'}]

for item in vlans:
    template=Template(templates)
    data = {'id': item['id']}
    net = ipcalc.IPCalc(item['ip'])
    data['net'] = net
    template=template.render(data=data)
    print(template)
