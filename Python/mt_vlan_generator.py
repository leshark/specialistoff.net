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
add interface=vlan{{ data['id'] }} address={{ data['gateway'] }}/{{ data['subnet'] }}

# Шейпер
/queue simple
add max-limit=3M/3M name=queue{{ data['id'] }} target=vlan{{ data['id'] }}

# DHCP
/ip pool
add name=pool2 ranges={{ data['range'][0] }}-{{ data['range'][1] }}
/ip dhcp-server
add address-pool=pool1 interface=bridge-local name=server1
/ip dhcp-server network
add address={{ data['broadcast'] }}/{{ data['subnet'] }} dns-server=77.88.8.8,77.88.8.1 gateway={{ data['gateway'] }} netmask={{ data['subnet'] }}

# NAT
/ip firewall address-list
add address={{ data['ip'] }}/24 list=vlans

/ip firewall nat
add action=src-nat chain=srcnat out-interface=WAN src-address-list=vlans to-addresses=XXX.XXX.XXX.XXX
# XXX.XXX.XXX.XXX - внешний IP
"""

vlans = [{'id': 70, 'ip': '192.168.0.0/24'},
{'id': 80, 'ip': '192.168.1.0/24'},
{'id': 90, 'ip': '192.168.2.0/24'},
{'id': 100, 'ip': '192.168.3.0/24'}]

for item in vlans:
    template=Template(templates)
    data = {'id': item['id']}
    net = ipcalc.Network(item['ip'])
    data['gateway'] = net.host_first()
    data['subnet'] = net.subnet()
    data['range'] = [net[2], net.host_last()]
    data['broadcast'] = net.info()
    template=template.render(data=data)
    print(template)
