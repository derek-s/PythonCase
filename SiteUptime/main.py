#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 22:25
# @Author  : Derek.S
# @Site    : SiteUptime Checker
# @File    : main.py

import pycurl
import argparse
import re
import subprocess
import itchat
import arrow
import time

# 初始化命令行交互
parser = argparse.ArgumentParser()

# 设定命令行参数及提示信息
parser.add_argument("url", type=str, help="Monitored domain name(url)")

# 获取命令行参数
args = parser.parse_args()

class Checker:
    """
    检查器
    """
    def __init__(self):
        # 初始化时读取命令行输入
        raw_url = args.url
        re_string = r"/"
        if re.findall(re_string, raw_url) == 0:
            self.url = raw_url
        elif re.findall(re_string, raw_url) != 1:
            self.url = args.url.split("/")[-1]

        # 开启日志
        self.log = Dylog()

        # 开启wechat及登陆
        self.wechat = weChat()
        self.wechat.login()

    def Ping_Testing(self):
        """
        Ping测试
        :return: 测试结果，不通为0，通为1
        """
        self.log.writelog(getDate(), self.url, "开始Ping测试")
        print("##### Ping %s Test #####" % (self.url))
        ping_test = "ping -c 5 -W 3 %s" % (self.url)
        subp = subprocess.Popen(
            ping_test,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        ping_result = str(subp.stdout.read()) # class byte to str
        ping_regex = re.findall("100% packet loss", ping_result)
        if len(ping_regex) == 0:
            print("##### Ping %s all green #####" % (self.url))
            self.log.writelog(getDate(), self.url, "Ping测试正常")
            return(1)
        else:
            print("##### Ping %s error #####" % (self.url))
            self.log.writelog(getDate(), self.url, "Ping测试失败 100% packet loss")
            self.wechat.send_mes(self.url + "Ping测试失败")
            return(0)

    def Curl_HttpTesting(self):
        """
        Curl HTTP测试
        测试连接、网站状态码、DNS解析时间、连接时间等
        :return:
        """

        curl = pycurl.Curl()

        # 将curl返回页面内容重定向到文件 pycutl.writexxx 为二进制写入，注意文件打开模式
        content = open("content", "wb")
        curl.setopt(pycurl.WRITEDATA, content)

        # 配置pycurl
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.CONNECTTIMEOUT, 5)  # 设置请求连接等待时间为5秒
        curl.setopt(pycurl.TIMEOUT, 5)  # 设置超时时间为5秒
        curl.setopt(pycurl.NOPROGRESS, 1)  # 关闭下载进度条
        curl.setopt(pycurl.FORBID_REUSE, 1)  # 交互后关闭连接，不重用连接
        curl.setopt(pycurl.MAXREDIRS, 1)  # 重定向最大次数为1次
        curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 5)  # 设置DNS缓存时间为5秒

        # work
        try:
            print("##### Curl %s Test #####" % (self.url))
            self.log.writelog(getDate(), self.url, "开始curl http状态测试")
            curl.perform()
            nslookup_time = str(round(curl.getinfo(curl.NAMELOOKUP_TIME), 2))
            connect_time = str(round(curl.getinfo(curl.CONNECT_TIME), 2))
            http_code = str(curl.getinfo(curl.HTTP_CODE))
            print("##### Curl %s all green #####" % (self.url))
            print(nslookup_time, connect_time, http_code)
            self.log.writelog(
                getDate(),
                self.url,
                "测试结束 状态码" + http_code + " DNS查询时间 " + nslookup_time + "秒 连接用时 " + connect_time + "秒"
            )
            content.close()
            curl.close()
        except Exception as e:
            print("##### Curl %s error #####" % (self.url) + " " +(str(e)))
            self.log.writelog(getDate(), self.url, "curl http状态测试失败 错误信息：" + str(e) )
            self.wechat.send_mes(self.url + "curl http测试失败" + str(e))
            content.close()
            curl.close()


class weChat:
    # 增加微信消息发送
    def login(self):
        itchat.auto_login(enableCmdQR=2)

    def send_mes(self,message):
        itchat.send(message, toUserName="filehelper")


class Dylog:
    # 日志系统(简单实现)
    def __init__(self):
        filename = str(arrow.now().format("YYYY-MM-DD")) + "_log.txt"
        self.logfile = open(filename, "a+", encoding="utf-8")

    def writelog(self, logdate, target, logmessage):
        logdate_str = "[" + str(logdate) + "] - " + target + " - " + logmessage
        self.logfile.write(logdate_str + "\n")

    def logfile_close(self):
        self.logfile.close()

def getDate():
    # 返回系统当前时间
    return str(arrow.now().format("YYYY-MM-DD HH:mm:ss"))


def testbase():
    checker = Checker()
    while(1):
        checker.Ping_Testing()
        checker.Curl_HttpTesting()
        time.sleep(60)


if __name__ == "__main__":
    testbase()