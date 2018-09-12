# #!/usr/bin/python
# -*- coding: utf-8 -*-
# File:main.py
# Project:zabbix_smsbao
# File Created:2018-09-12 04:54:36
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2018-09-12 04:54:36
# -----

import requests


def sendSms(phoneNumber, content):
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }


    smsapi = "http://api.smsbao.com/sms?"
    user = ""
    pwd = ""

    params = {"u":user, "p":pwd, "m":phoneNumber, "c":content}

    r = requests.get(smsapi, params=params)
    print(r.text)
    print(statusStr[r.text])


if __name__ == "__main__":
    sendSms("手机号码", "短信内容")