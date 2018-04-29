from machine import Pin
import machine
import utime
import varibles as vars
import neopixel
import urequests
import ubinascii

# Neo pixels
neoPin = 14  # D5

np = neopixel.NeoPixel(Pin(neoPin), 8)

neoLow = 0  # type: int
neoMid = 64  # type: int
neoHi = 255  # type: int

red = (neoMid, neoLow, neoLow)
yellow = (255, 226, neoLow)
tango = (243, 114, 82)
green = (neoLow, neoMid, neoLow)
indigo = (neoLow, 126, 135)
blue = (neoLow, neoLow, neoMid)
purple = (neoMid, neoLow, neoMid)
black = (neoLow, neoLow, neoLow)

# Battery voltage
voltageraw = 0.0  # type: float
voltagereading = 0.0  # type: float
voltagemultiplier = 10.0  # type: float

functionStateChanged = False


def getbatteryvoltage():
    voltageraw = machine.ADC(0)

    voltagereading = voltageraw * voltagemultiplier


def main():
    # Set initial state
    np[0] = purple
    np[1] = purple
    np[2] = purple
    np[3] = red

    np.write()

    sensorValueLast = 0

    while True:

        getbatteryvoltage()

        print('Battery voltage: {0}'.replace('{0}', str(voltageraw)))

        utime.sleep(10000)


main()
