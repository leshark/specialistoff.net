#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'

class IPCalc():
    def __init__(self, addr, cidr = None):
        overloads = addr.split('/')
        if len(overloads)>1:
            cidr = overloads[1]
            addr = overloads[0]
        self.addr = addr.split('.')
        self.cidr = int(cidr)
        self.calc()

    def __iter__(self):
        pass

    def __getitem__(self, key):
        result = self.net[::-1]
        i=0
        while key > 0:
            result[i] += key % 256
            key = key >> 8
            i +=1
        result = result[::-1]
        return '.'.join(map(str, result))

    @property
    def Address(self):
        return '.'.join(self.addr)

    @property
    def Bitmask(self):
        return self.cidr

    @property
    def Netmask(self):
        return '.'.join(map(str, self.mask))

    @property
    def Wildcard(self):
        return '.'.join(map(str, self.inmask))

    @property
    def Network(self):
        return '.'.join(map(str, self.net))

    @property
    def FirstIP(self):
        return '.'.join(map(str, self.firstip))

    @property
    def LastIP(self):
        return '.'.join(map(str, self.lastip))

    @property
    def Broadcast(self):
        return '.'.join(map(str, self.broad))

    @property
    def Addresses(self):
        return self.addresses

    @property
    def Hosts(self):
        return self.hosts

    def calc(self):
        # Подсчет маски
        self.mask = [0, 0, 0, 0]
        for i in range(self.cidr):
            self.mask[int(i/8)] = self.mask[int(i/8)] + (1 << (int(7 - i % 8)))

        # Подсчет инверсной маски
        self.inmask = [255, 255, 255, 255]
        for i in range(self.cidr):
            self.inmask[int(i/8)] = self.inmask[int(i/8)] - (1 << (int(7 - i % 8)))

        # Подсчет сети
        # IP AND MASK
        self.net = []
        for i in range(4):
            self.net.append(int(self.addr[i]) & self.mask[i])

        # Подсчёт broadcast
        # NET OR INVERT MASK
        self.broad = []
        for i in range(4):
            self.broad.append(self.net[i] | self.inmask[i])

        # Первый хостовый IP
        self.firstip = self.net[:]
        self.firstip[3] = self.firstip[3] | 1

        # Последний хостовый IP
        self.lastip = self.broad[:]
        self.lastip[3] = self.lastip[3] & (255 - 1)

        # Количество адресов
        # 2^(32 - netmask_length) - 2
        self.addresses = (1 << (32 - self.cidr))

        # Количество хостовых адресов
        # 2^(32 - netmask_length) - 2
        self.hosts = self.addresses - 2
        if self.hosts < 2:
            self.hosts = None

    def __str__(self):
        return "%s/%s" % (self.Address, self.Netmask)

    def __repr__(self):
        result = []
        result.append("IP-адрес: %s" % (self.Address))
        result.append("Маска: %s" % (self.Bitmask))
        result.append("Маска подсети: %s" % (self.Netmask))
        result.append("Wildcard: %s" % (self.Wildcard))
        result.append("Адрес сети: %s" % (self.Network))
        result.append("Первый IP: %s" % (self.FirstIP))
        result.append("Последний IP: %s" % (self.LastIP))
        result.append("Broadcast: %s" % (self.Broadcast))
        result.append("Количество адресов: %s" % (self.Addresses))
        result.append("Количество хостовых адресов: %s" % (self.Hosts))
        return '\n'.join(result)
