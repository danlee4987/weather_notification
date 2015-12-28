#!/usr/bin/python

import sys
sys.dont_write_bytecode = True

from notificationHandler import notify
from notificationHandler import clearNotifications
import pyowm

def initializeWatWeather():
    owm = pyowm.OWM('600e3e07733d9300360d021d7de61472')
    observation = owm.weather_at_place('Waterloo,ca')
    w = observation.get_weather()
    return w
