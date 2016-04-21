#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

'''Генератор VirtualHosts

Пример применения шаблонов
'''

import os
import sys

from jinja2 import Template


template = """<VirtualHost *:8080>
    ServerAdmin info@{{ domain }}
    DocumentRoot "/home/{{ user }}/{{ domain }}"
    ServerName {{ domain }}
    ServerAlias www.{{ domain }}
    ErrorLog "/var/log/httpd/domains/{{ domain }}-error.log"
    CustomLog "/var/log/httpd/domains/{{ domain }}-access.log" common
    AcceptPathInfo On
    <Directory /home/{{ user }}/{{ domain }}>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
"""

data = [{'user': 'viktor',
            'domains': ['sys-center.ru']},
        {'user': 'eri',
            'domains': ['eerie.su']},
        {'user': 'remizoffalex',
            'domains': ['remizoffalex.ru', 'specialistoff.net']}
    ]

for item in data:
    for domain in item['domains']:
        config=Template(template)
        config=config.render(user=item['user'], domain=domain)
        print(config)
