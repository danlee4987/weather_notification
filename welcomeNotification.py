#!/usr/bin/python

import sys
sys.dont_write_bytecode = True
import time
from notificationHandler import notify
from notificationHandler import clearNotifications
import weatherHandler
import os
import urllib

def log_to_file(message):
    currTime = time.ctime()[11:16]
    with open("/Users/danlee/Documents/GitHub/weather_notification/logs/weather_notification.log", "a") as log:
        log.write('{0}: {1}\n'.format(currTime, message))

def internet_on():
    '''
    Makes sure an internet connection exists
    '''
    try :
        log_to_file('Checking for internet connection...')

        url = "https://www.google.ca"
        data = urllib.urlopen(url)
        log_to_file('Connection exists!')
        return True

    except Exception as e:
        log_to_file('Connection does not exist! {0}'.format(e.message))

def calcSecsTilNextHour():
    '''
    Calculates seconds until next hour, needed until new method is found
    '''
    secsInHour = 3600
    hourToSecs = int(time.ctime()[14:16])*60
    secs = int(time.ctime()[17:19])
    secsLeft = secsInHour - hourToSecs + secs
    log_to_file('Seconds to next hour: {0}'.format(secsLeft))
    return secsLeft

def calcCurrentTime():
    '''
    Calculates current hour, minute, and second
    '''
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

    currTime = [str(hour), str(minute), str(period)]
    return currTime

def getTime(hour):
    '''
    Calculates message to be displayed in notification depending on time
    '''
    if hour >= 6 and hour < 12:
        return "Good Morning!"

    elif hour >= 12 and hour < 17:
        return "Good Afternoon!"

    elif hour >= 17 and hour < 23:
        return "Good Evening!"

    elif hour >= 23 or (hour >= 0 and hour < 6):
        return "Good Night!"

    else:
        raise Exception("ERROR: Time detected: {0}".format(hour))

def notificationLauncher(secsLeft):
    '''
    Displays weather and time once every hour
    '''
    w = weatherHandler.initializeWatWeather()
    currentTemp = str(w.get_temperature('celsius')['temp'])
    currentStatus = w.get_detailed_status().title()

    clearNotifications()
    currTime = calcCurrentTime()

    message = getTime(currTime[0])

    log_to_file('Outputting notification...')
    notify(message, currentStatus,
    "Temp is %s degrees right now" %currentTemp, sound=False)

    if secsLeft == 3600:
        # message for when on the hour
        os.system('say "Currently %s, %s, and it is %s degrees with %s"'
        %(currTime[0], currTime[2], currentTemp, currentStatus))
    else:
        # message if time is not on the hour
        os.system('say "Currently %s, %s %s, and it is %s degrees with %s"'
        %(currTime[0], currTime[1], currTime[2], currentTemp, currentStatus))

    # need to figure out how to launch script once an hour w/o sleeping
    time.sleep(secsLeft)

def main():
    loop_counter = 0
    for i in range(0,5):
        if internet_on():
            break
        time.sleep(20)

    while True:
        secsLeft = calcSecsTilNextHour()
        try:
            notificationLauncher(secsLeft)
        except Exception as e:
            log_to_file(e.message)
            sys.exit(1)

if __name__ == '__main__':
    main()
