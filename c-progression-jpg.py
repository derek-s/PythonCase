#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-12-23 23:17+08:00
# @Author  : Derek.S
# @Site    : https://www.dadclab.com
# @File    : c-progression-jpeg.py
# @Software: convert JPEG to progression JPEG


import os
from PIL import Image

catalog = os.walk(r".")

for path, dir_list, file_list in catalog:
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == ".jpg":
            name = path+ '/' + file_name
            print name
            try:
                im = Image.open(name)
                im.save(name, 'JPEG', progressive=True, optimize=True, quality=90)
            except IOError:
                pass
        elif os.path.splitext(file_name)[1] == ".JPG":
            name = path+ '/' + file_name
            print name
            try:
                im = Image.open(name)
                im.save(name, 'JPEG', progressive=True, optimize=True, quality=90)
            except IOError:
                pass
        else:
            print 'error' + file_name
