#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'RemiZOffAlex'
__copyright__ = '(c) RemiZOffAlex'
__license__ = 'MIT'
__email__ = 'remizoffalex@mail.ru'
__url__ = 'http://remizoffalex.ru'

from lxml import etree, html

class Escape():
    def __init__(self, text):
        self.text = text
        self.error = False
        try:
            root = html.fromstring('<root>' + self.text + '</root>')
            for bad in root.xpath("//script"):
                print(bad.text)
                bad.getparent().remove(bad)
            for bad in root.xpath("//form"):
                print(bad.text)
                bad.getparent().remove(bad)
            for bad in root.xpath("//@onclick"):
                print(bad)
                print(bad.is_attribute)
                print(bad.getparent())
                # print(bad.getparent().is_attribute)
                # Удалить атрибут onclick
                bad.getparent().attrib.pop('onclick')
        except etree.XMLSyntaxError as error:
            self.text = 'Данные некорректны:<br/>'
            for item in error.error_log:
                msg = ''.join([
                    '<p>Ошибка: ', item.message,
                    ' в ', str(item.line),
                    ' строке ', str(item.column), ' колонке'
                ])
                self.text = self.text + msg
            self.error = True
        else:
            self.text = html.tostring(root, encoding='utf-8').decode('utf-8')
            self.text = self.text[6:]
            self.text = self.text[:-7]

    def __repr__(self):
        return self.text

    def tostring(self):
        return self.text
