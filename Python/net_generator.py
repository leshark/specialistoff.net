#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

'''
Генератор конфигурационного файла для сетевых интерфейсов

Пример применения шаблонов
'''

import os
import sys
import argparse
import traceback
import ipcalc

from jinja2 import Environment, FileSystemLoader

def generate(os, listip, templatedir):
    j2_env=Environment(loader=FileSystemLoader(templatedir),
                     trim_blocks=True)
    for i, line in enumerate(listip):
        net = ipcalc.IPCalc(line)
        template=j2_env.get_template(os + '.interfaces.template').render(i=i, net=net)
        print(template)

def main():
    parser = argparse.ArgumentParser(description='Генератор конфигурационного файла для сетевых интерфейсов',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = "Необязательные аргументы"

    parser.add_argument("--ipv4", nargs='+', dest="ipv4", required=True, help="IP v4")
    parser.add_argument("--os", dest="os", required=True, help="Операционная система")
    parser.add_argument("--tmpldir",
        dest="tmpldir",
        default=os.path.dirname(os.path.abspath(__file__)) + "/templates",
        help="Каталог шаблонов")

    args = parser.parse_args()

    generate(args.os, args.ipv4, args.tmpldir)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        traceback.print_exc(file=sys.stdout)
        exit(1)

    exit(0)
