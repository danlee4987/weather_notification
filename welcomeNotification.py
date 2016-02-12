#!/usr/bin/python

import sys
sys.dont_write_bytecode = True
import time
from notificationHandler import notify
from notificationHandler import clearNotifications
import weatherHandler
import os
import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.43.79',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def calcSecsTilNextHour():
    secsInHour = 3600
    hourToSecs = int(time.ctime()[14:16])*60
    secs = int(time.ctime()[17:19])
    secsLeft = secsInHour - hourToSecs + secs
    return secsLeft

def calcCurrentTime():
    period = ""
    minute = int(time.ctime()[14:16])
    hour = int(time.ctime()[11:13])
    if hour > 12:
        hour = hour - 12
        period = "PM"
    elif hour == 24 or hour == 0:
        hour = 12
        period = "AM"
    else:
        hour = hour
        period = "AM"

    currTime = []
    currTime.append(str(hour))
    currTime.append(str(minute))
    currTime.append(str(period))
    return currTime

def notificationLauncher(secsLeft):
    hour = int(time.ctime()[11:13])
    #date = time.ctime()[0:10]

    w = weatherHandler.initializeWatWeather()
    currentTemp = str(w.get_temperature('celsius')['temp'])
    currentStatus = w.get_detailed_status().title()

    clearNotifications()
    if hour >= 6 and hour < 12:
        notify("Good Morning!", currentStatus,
        "Temp is %s degrees right now" %currentTemp, sound=False)

    elif hour >= 12 and hour < 17:
        notify("Good Afternoon!", currentStatus,
        "Temp is %s degrees right now" %currentTemp, sound=False)

    elif hour >= 17 and hour < 23:
        notify("Good Evening!", currentStatus,
        "Temp is %s degrees right now" %currentTemp, sound=False)

    elif hour >= 23 or (hour >= 0 and hour < 6):
        notify("Good Night!", currentStatus,
        "Temp is %s degrees right now" %currentTemp, sound=False)

    else:
        notify("Welcome Notification",
        "Error!", "Check logs to debug", sound=True)
        sys.exit()

    currTime = calcCurrentTime()

    if secsLeft == 3600:
        os.system('say "Currently %s, %s, and it is %s degrees with %s"'
        %(currTime[0], currTime[2], currentTemp, currentStatus))
    else:
        os.system('say "Currently %s, %s %s, and it is %s degrees with %s"'
        %(currTime[0], currTime[1], currTime[2], currentTemp, currentStatus))

    time.sleep(secsLeft)

if __name__ == '__main__':
    loop_counter = 0
    for i in range(0,5):
        if internet_on():
            break
        time.sleep(20)

    while True:
        secsLeft = calcSecsTilNextHour()
        notificationLauncher(secsLeft)
