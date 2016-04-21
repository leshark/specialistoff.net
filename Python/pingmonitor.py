#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

"""
pip3 install rrdtool psutil
"""

import os
import time
import rrdtool
import subprocess

fname = 'database.rrd'  

ip = '8.8.8.8'

if not os.path.isfile(fname):
    rrdtool.create(
        fname,
        # шаг 300с — данные, хранимые в БД будут привязаны к «сетке», шагом в пять минут
        "--step", "10s",
        # Источник
        # cpu - название источника
        # type - GAUGE
        # heartbeat - 5m
        # min, max - предельные значения
        'DS:ping:GAUGE:1m:0:65535',
        # описываем какие отчёты хотим хранить в БД. 
        # последние 48 часов, каждые 5 мин
        # 0.5 - xff
        # 576 (48 часов и каждые 5 минут)
        'RRA:AVERAGE:0.5:1m:2d',
        'RRA:MAX:0.5:1m:2d'
        )

def getping(IP):
    result = False
    p = subprocess.Popen(["/bin/fping", "-e", IP], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output,error = p.communicate()
    val = output.decode("utf-8").split(" ")
    if val[2] == "alive":
        result = val[3][1:]
    return result

while True:

    val = getping(ip)
    print(val)

    if val:
        rrdtool.update(fname, '-t', 'ping', 'N:' + str(val))


    rrdtool.graph( 'graph.png',
        # За какой период показать график: 30 минут
        "--start", "-1d",
        "--title", "Ping",
        "--disable-rrdtool-tag",
        "--imgformat" , "PNG" ,
        # "--vertical-label=CPU",
        "--watermark", "http://SpecialistOff.NET/ from http://RemiZOffAlex/",
        "-w 800",  "-h 300",
        "DEF:valping1=" + fname + ":ping:AVERAGE",
        "DEF:valping2=" + fname + ":ping:MAX",
        # Заливка области
        "AREA:valping1#00FF00:Время ответа среднее",
        "LINE1:valping2#FF0000:Время ответа максимальное")

    time.sleep(10)
