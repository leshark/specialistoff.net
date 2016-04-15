#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

"""
pip3 install rrdtool
"""

import os
import time
import rrdtool
# Библиотека получения информации о нагрузке системы
import psutil

fname = 'database.rrd'  

if not os.path.isfile(fname):
    rrdtool.create(
        fname,
        # шаг 300с — данные, хранимые в БД будут привязаны к «сетке», шагом в пять минут
        "--step", "5s",
        # Источник
        # cpu - название источника
        # type - GAUGE
        # heartbeat - 5m
        # min, max - предельные значения
        'DS:cpu:GAUGE:1m:0:100',
        # описываем какие отчёты хотим хранить в БД. 
        # последние 48 часов, каждые 5 мин
        # 0.5 - xff
        # 576 (48 часов и каждые 5 минут)
        'RRA:AVERAGE:0.5:1m:2d',
        'RRA:MAX:0.5:1m:2d'
        )

while True:
    val = psutil.cpu_percent(interval=1)
    print(val)

    rrdtool.update(fname, '-t', 'cpu', 'N:' + str(val))


    rrdtool.graph( 'graph.png',
        # За какой период показать график: 30 минут
        "--start", "-16h",
        "--title", "CPU",
        "--disable-rrdtool-tag",
        "--imgformat" , "PNG" ,
        # "--vertical-label=CPU",
        "--watermark", "http://SpecialistOff.NET/ from RemiZOffAlex (http://remizoffalex.ru/)",
        "-w 800",  "-h 300",
        "DEF:valcpu1=" + fname + ":cpu:AVERAGE",
        "DEF:valcpu2=" + fname + ":cpu:MAX",
        # Заливка области
        "AREA:valcpu1#00FF00:CPU среднее",
        "LINE1:valcpu2#FF0000:CPU максимальное")

    time.sleep(3)
