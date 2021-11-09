#!/usr/bin/env python3

import sys
import time
import board
import busio
import spidev
import adafruit_tsl2591

spi = spidev.SpiDev()
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2591.TSL2591(i2c)

def leddat(rvalue, gvalue, bvalue, rgain, ggain, bgain):
    bytes = [];
    for x in range(16):
        bytes.append(0)
    gain = 0x8000 | (rgain<<10) | (ggain<<5) | (bgain)
    for x in range(8):
        bytes.append( (gain >> 8) & 0xFF)
        bytes.append( (gain >> 0) & 0xFF)
        bytes.append( (rvalue >> 8 ) & 0xFF)
        bytes.append( (rvalue >> 0 ) & 0xFF)
        bytes.append( (gvalue >> 8 ) & 0xFF)
        bytes.append( (gvalue >> 0 ) & 0xFF)
        bytes.append( (bvalue >> 8 ) & 0xFF)
        bytes.append( (bvalue >> 0 ) & 0xFF)
    return bytes

def settleToBlack():
    while True:
        spi.writebytes2(leddat(0, 0, 0, 0, 0, 0))
        lux = sensor.lux
        if lux == 0:
            break

def getLux(rvalue, gvalue, bvalue, rgain, ggain, bgain, settleTime):
    lux = 0
    # wait until everything is completely dark
    settleToBlack()
    while True:
        spi.writebytes2(leddat(rvalue, gvalue, bvalue, rgain, ggain, bgain))
        # wait until we stabilize
        time.sleep(settleTime)
        lux = sensor.lux
        if (lux != 0):
            break
    return lux

def main():

    spi.open(0,0)
    spi.bits_per_word = 8
    spi.max_speed_hz = 4000000

    sensor.gain = 0x20
    sensor.integration_time = 0x0

    rgain = 31
    ggain = 31
    bgain = 31

    f = open("hd108data_g{}i{}rg{}gg{}bg{}.txt".format(sensor.gain>>4,sensor.integration_time,rgain,ggain,bgain), "w")

    settleToBlack()

    # first section with highest gain
    for i in range(1,1024,1):
        rlux = getLux(i, 0, 0, rgain, ggain, bgain, 0.2)
        glux = getLux(0, i, 0, rgain, ggain, bgain, 0.2)
        blux = getLux(0, 0, i, rgain, ggain, bgain, 0.2)
        print("i:{} r:{:0.5f} g:{:0.5f} b{:0.5f}".format(i, rlux, glux, blux))
        f.write("{},{:0.5f},{:0.5f},{:0.5f}\n".format(i, rlux, glux, blux))
        f.flush()
    
    f.close()

if __name__ == '__main__':
    sys.exit(main())