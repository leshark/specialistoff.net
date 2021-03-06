#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

import sys
import argparse
from crmapp import app, lib, models

def main():
    parser = argparse.ArgumentParser(description='Скрипт сброса пароля пользователя',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = "Необязательные аргументы"

    parser.add_argument("--user", dest="user", help="Пользователь")
    parser.add_argument("--password", dest="password", help="Новый пароль")

    args = parser.parse_args()

    user = models.db_session.query(
        models.User
    ).filter(
        models.User.name==args.user
    ).first()
    if user:
        user.password = lib.get_hash_password(args.password,
            app.config['SECRET_KEY'])
        models.db_session.commit()
        print('Пароль изменён')

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        traceback.print_exc(file=sys.stdout)
        exit(1)

    exit(0)
