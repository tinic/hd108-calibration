#!/usr/bin/env python3

import sys
import time
import board
import busio
import adafruit_tsl2591
 
def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tsl2591.TSL2591(i2c)
    while True:
        lux = sensor.lux
        print("Total light: {0}lux".format(lux))
        infrared = sensor.infrared
        print("Infrared light: {0}".format(infrared))
        visible = sensor.visible
        print("Visible light: {0}".format(visible))
        full_spectrum = sensor.full_spectrum
        print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
        time.sleep(1.0)

if __name__ == '__main__':
    sys.exit(main())
