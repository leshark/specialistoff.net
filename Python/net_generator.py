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

def generate4(os, listip, iface, templatedir, num=0):
    j2_env=Environment(loader=FileSystemLoader(templatedir),
                     trim_blocks=True)
    for i, line in enumerate(listip):
        net = ipcalc.IPCalcV4(line)
        net.version='v4'
        template = None
        if os in ['debian', 'ubuntu']:
            template=j2_env.get_template('debian.interfaces.template').render(i=(i+num), net=net, iface=iface)
        else:
            template=j2_env.get_template(os + '.interfaces.template').render(i=(i+num), net=net, iface=iface)
        print(template)

def generate6(os, listip, iface, templatedir):
    """Не сделан калькулятор ip v6"""
    j2_env=Environment(loader=FileSystemLoader(templatedir),
                     trim_blocks=True)
    for i, line in enumerate(listip):
        #net = ipcalc.IPCalcV4(line)
        net = {'version': 'v6', 'Address': line, 'Netmask': '48'}
        template=j2_env.get_template(os + '.interfaces.template').render(i=i, net=net, iface=iface)
        print(template)

def main():
    parser = argparse.ArgumentParser(description='Генератор конфигурационного файла для сетевых интерфейсов',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = "Необязательные аргументы"

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ipv4", nargs='+', dest="ipv4", help="IP v4")
    group.add_argument("--ipv6", nargs='+', dest="ipv6", help="IP v6")
    parser.add_argument("--os", dest="os", required=True, help="Операционная система")
    parser.add_argument("--iface", dest="iface", default="eth0", help="Операционная система")
    parser.add_argument("--num", dest="num", type=int, default=0, help="Номер")
    parser.add_argument("--tmpldir",
        dest="tmpldir",
        default=os.path.dirname(os.path.abspath(__file__)) + "/templates",
        help="Каталог шаблонов")
    parser.add_argument("--maskv4", dest="maskv4", default='24', help="Mask v4")

    args = parser.parse_args()

    if args.os not in ['centos', 'debian', 'fedora', 'ubuntu']:
        raise Exception("Указанного значения нет в списке допустимых ОС\nНеобходимо указать centos, debian, fedora, ubuntu")

    if args.ipv6:
        generate6(args.os, args.ipv6, args.iface, args.tmpldir)
    elif args.ipv4:
        ipv4list = args.ipv4
        if args.maskv4:
            for i, item in enumerate(ipv4list):
                ipv4list[i] = item + '/' + args.maskv4
        print(ipv4list)
        generate4(args.os, ipv4list, args.iface, args.tmpldir, args.num)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        traceback.print_exc(file=sys.stdout)
        exit(1)

    exit(0)
