#!/usr/bin/env python3

"""
Trilby Tanks 2018 copyright
Module: tankMoisture
"""

from machine import Pin
from machine import RTC
import network
import machine
import utime
#  import varibles as vars
import urequests
import ubinascii
from heartbeatClass import HeartBeat
from timeClass import TimeTank
from SensorRegistationClass import SensorRegistation
from NeoPixelClass import NeoPixel

restHost = "http://192.168.86.240:5000"  # /{0}/"

moisturePin = Pin(13, Pin.IN, Pin.PULL_UP)  # D7

neoPin = 12  # D6
np = NeoPixel(neoPin, 2)

powerLed = 0
moistureLed = 1

# Set initial state
np.colour(powerLed, 'red')
np.colour(moistureLed, 'purple')
np.write()

sensorname = 'moisture001'

# lastmoisture = 0


def getdeviceid():

    deviceid = ubinascii.hexlify(machine.unique_id()).decode()
    deviceid = deviceid.replace('b\'', '')
    deviceid = deviceid.replace('\'', '')

    return deviceid


def getip():
    sta_if = network.WLAN(network.STA_IF)
    temp = sta_if.ifconfig()

    return temp[0]


def testfornetwork():
    sta_if = network.WLAN(network.STA_IF)
    while not sta_if.active():
        print('Waiting for Wifi')

    while '0.0.0.0' == getip():
        print('Waiting for IP')


def moistureCallBack(p):
    # global lastmoisture
    currentmoisture = moisturePin.value()
    sensorvalue = 0
    print("currentmoisture = ", currentmoisture)

    if currentmoisture == 1:
        print("no water...")
        sensorvalue = 0
        np.colour(moistureLed, 'purple')
    else:
        print("blue gold, we struck water!!!")
        sensorvalue = 1
        np.colour(moistureLed, 'blue')

    np.write()

    url = restHost + "/sensorStateWrite/{0}/{1}/{2}"
    url = url.replace('{0}', getdeviceid())  # sensor id
    url = url.replace('{1}', sensorname)  # sensor type
    url = url.replace('{2}', str(sensorvalue))  # sensor value

    print(url)

    try:
        response = urequests.get(url)

        print(response.text)

        response.close()
    except:
        print('Fail www connect...')

        # lastmoisture = currentmoisture


def main():
    # Set initial state
    testfornetwork()

    deviceid = getdeviceid()

    mySensorRegistation = SensorRegistation(restHost, deviceid)
    mySensorRegistation.register(sensorname, 'Hardware', 'JH')

    myheartbeat = HeartBeat(restHost, deviceid)
    myheartbeat.beat()

    mytime = TimeTank(deviceid)
    while not mytime.settime():
        pass

    rtc = RTC()
    sampletimes = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56]
    samplehours = [1, 6, 12, 18]
    isMinuteProcess = 0
    lastMin = 0
    gethour = 0

    moisturePin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=moistureCallBack)

    while True:
        timeNow = rtc.datetime()
        currHour = timeNow[4]
        currMinute = timeNow[5]

        if currMinute not in sampletimes and isMinuteProcess == 0:
            # process goes here

            isMinuteProcess = 1

        if currMinute in sampletimes and isMinuteProcess == 1:
            # process goes here

            isMinuteProcess = 0

        if lastMin != currMinute:
            # process goes here
            myheartbeat.beat()

            lastMin = currMinute

        if currHour not in samplehours and gethour == 0:
            gethour = 1

        if currHour in samplehours and gethour == 1:
            gethour = 0
            local = utime.localtime()
            while not mytime.settime():
                pass


main()
