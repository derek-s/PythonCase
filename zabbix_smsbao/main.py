#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:main.py
# Project:zabbix_smsbao
# File Created:2018-09-12 04:54:36
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2018-09-12 04:54:36
# -----

import requests
import sys


def sendSms(phoneNumber, content):
    statusStr = {
        '0': '0',
        '-1': '-1',
        '-2': '-2',
        '30': '30',
        '40': '40',
        '41': '41',
        '42': '42',
        '43': '43',
        '50': '50'
    }


    smsapi = "http://api.smsbao.com/sms?"
    user = ""
    pwd = ""

    params = {"u":user, "p":pwd, "m":phoneNumber, "c":content}

    r = requests.get(smsapi, params=params)
    #print(r.text)
    #print(statusStr[r.text])


if __name__ == "__main__":
    sendSms(sys.argv[1],sys.argv[2])