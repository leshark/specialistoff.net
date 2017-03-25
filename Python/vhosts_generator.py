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

from jinja2 import Environment, FileSystemLoader


templatedir = os.path.dirname(os.path.abspath(__file__)) + "/templates"
templates = ['apache.vhosts.template', 'nginx.vhosts.template']

data = [
    {
        'user': 'remizoffalex',
        'domains': [
            'remizoffalex.ru', 'specialistoff.net', 'wiki.specialistoff.net'
        ]
    }
]

for item in data:
    for domain in item['domains']:
        j2_env=Environment(
            loader=FileSystemLoader(templatedir),
            trim_blocks=True)
        for template in templates:
            config=j2_env.get_template(template).render(user=item['user'], domain=domain)
            print('Шаблон: ' + template)
            print(config)
