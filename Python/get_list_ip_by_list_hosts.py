#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import dns.resolver

hosts = [
    'ask.fm',
    'facebook.com',
    'fbcdn.net',
    'flickr.com',
    'instagram.com',
    'LiveInternet.ru',
    'mamba.ru',
    'mirtesen.ru',
    'moikrug.ru',
    'my.mail.ru',
    'pikabu.ru',
    'tumblr.com',
    'twitter.com',
    'ok.ru',
    'ok-portal.mail.ru',
    'vk.com',
    'vkrugudruzei.ru',
    'yaplakal.com'
]

try:
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ['77.88.8.8', '8.8.8.8']
    for host in hosts:
        answers = my_resolver.query(host, 'A')
        for rdata in answers:
            print(rdata.address)
except:
    pass
