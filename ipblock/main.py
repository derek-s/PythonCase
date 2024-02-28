#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: main.py
# DATE: 2024/02/27
# TIME: 12:59:46

# DESCRIPTION: 

import time
import psutil
import subprocess
import redis


historyRecord = set()

def get_ip_count(logFile, countDict, timestamp, redisClient):
    output = subprocess.Popen(["tail", "-n", "50", logFile], stdout = subprocess.PIPE).communicate()[0]
    lastRows = output.decode().split("\n")
    for eachRow in lastRows:
        if(len(eachRow) != 0 and eachRow not in historyRecord):
            historyRecord.add(eachRow)
            visitIP = eachRow.split()[0]
            visitURL = eachRow.split()[6]
            visitTime = int(time.mktime(time.strptime(eachRow.split()[3].split("[")[1], "%d/%b/%Y:%H:%M:%S")))
            # 爬虫访问的URL中的特征
            if("/tag/" in visitURL or "/wp-login.php" in visitURL or "/xmlrpc.php" in visitURL or "?replytocom=" in visitURL):
                # print(str(visitIP) + ":" + visitURL)
                # 判断时间 有数秒的延迟
                if(int(visitTime) >= timestamp - 10 or int(visitTime) <= timestamp + 10):
                    if(str(visitIP) in countDict):
                        # 计数
                        countDict[str(visitIP)] += 1
                    else:
                        countDict[str(visitIP)] = 1

    print(countDict)

    for eachIP in countDict:
        if (countDict[eachIP] > 20):
            with open("testPython.log", "a+") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S") + " - " + eachIP + " black\n")
            redisClient.set("bk:"+eachIP, "black")



if __name__ == "__main__":
    print("monitoring.....")
    redisHost = "127.0.0.1"
    redisPort = 6379
    redisDB = 1
    r = redis.StrictRedis(host=redisHost, port=redisPort, db=redisDB)
    d = {}

    while True:
        cpuRate = psutil.cpu_percent()
        if(cpuRate > 90):
            highTime = int(time.mktime(time.localtime()))
            print(time.strftime("%Y-%m-%d %H:%M:%S") + "cpu:" + str(cpuRate) + "%")
            get_ip_count("/home/wwwlogs/access.log", d, highTime, r)
        else:
            d = {}
            historyRecord.clear()
        time.sleep(1)

