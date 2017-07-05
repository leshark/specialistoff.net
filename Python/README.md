* get_hash_password.py - SHA-512 хеш пароля
* mail_log.py - лог подключения к почтовому сервису
* minimonitor.py - Мониторинг CPU с помощью rrdtool с построением графика

## net_generator.py

```sh
> python3 Python/net_generator.py --os debian --ipv4 1.2.3.4/16
auto eth0:0
iface eth0:0 inet static
        address 1.2.3.4
        netmask 255.255.0.0```

* get_list_ip_by_list_hosts.py - Получить список IP по списку хостов. На примере социальных сетей
* passgen.py - генератор пароля
* pingmonitor.py - Мониторинг доступности ресурса с помощью утилит fping и rrdtool с построением графика
* uploadtmplftp.py - генерирование файла по шаблону и загрузка данных на FTP сервер
* vhosts_generator.py - Конфигуратор виртуальных хостов для Apache
