#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import random

def pwgen(length=15):
    """
    Генератор пароля
    """
    alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    password=[]

    while len(password) < length:
        a_char = random.choice(alphabet)
        password.append(a_char)
    return ''.join(password)

print(pwgen())
