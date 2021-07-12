#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: main.py
# DATE: 2021/07/06
# TIME: 13:10:49

# DESCRIPTION: bilibili cc subtitle convert srt

import json
import datetime


def ConvertTime(seconds):
    """ Conver seconds to str subtittle format
        Args:
            seconds: float/int seconds
        Returns:
            a string
    """
    timeRaw = str(datetime.timedelta(seconds=seconds))
    timeSplit = timeRaw.split(".")
    if(len(timeSplit) == 1):
            timeSplit.append("000")
    if(len(timeSplit[1]) >= 3):
        timeStr = timeSplit[0] + "," + timeSplit[1][0:3]
    elif(len(timeSplit[1]) < 3):
        timeStr = timeSplit[0] + "," + timeSplit[1].ljust(3, "0")
    return str(timeStr)

# bcc file change expanded name to json
with open("test.json", "r") as j:
    subJson = json.load(j)
    j.close()

jsonBody = subJson["body"]

# output srt file
with open("test.srt", "w") as s:
    for i in range(1, len(jsonBody)):
        s.write(str(i) + "\n")
        s.write(
            ConvertTime(jsonBody[i]["from"]) + "-->" + ConvertTime(jsonBody[i]["to"]) + "\n"
        )
        s.write(
            jsonBody[i]["content"] + "\n"
        )
        s.write("\n")

    s.close()

