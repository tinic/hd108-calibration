#!/usr/bin/env python3

import sys
import time
import board
import busio
import spidev
import adafruit_tsl2591

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

def lux(spi, sensor, rvalue, gvalue, bvalue, rgain, ggain, bgain):
    lux = 0
    # wait until everything is completely dark
    while True:
        spi.writebytes2(leddat(0, 0, 0, rgain, ggain, bgain))
        lux = sensor.lux
        if lux == 0:
            break
    # wait until we stabilize
    while True:
        spi.writebytes2(leddat(rvalue, gvalue, bvalue, rgain, ggain, bgain))
        time.sleep(0.2)
        lux = sensor.lux
        if (lux != 0):
            break
    return lux

def main():

    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.bits_per_word = 8
    spi.max_speed_hz = 4000000

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tsl2591.TSL2591(i2c)

    sensor.gain = 0x10
    sensor.integration_time = 0x0

    sleep_time = 1

    rgain = 31
    ggain = 31
    bgain = 31

    f = open("hd108data_gain{}_int{}_rg{}_gg{}_bg{}.txt".format(sensor.gain,sensor.integration_time,rgain,ggain,bgain), "w")

    for i in range(16):
        spi.writebytes2(leddat(0, 0, 0, rgain, ggain, bgain))
        time.sleep(0.1)
        sensor.lux

    for i in range(3,65536,1):
        rlux = lux(spi,sensor,i,0,0,rgain, ggain, bgain)
        glux = lux(spi,sensor,0,i,0,rgain, ggain, bgain)
        blux = lux(spi,sensor,0,0,i,rgain, ggain, bgain)
        print("i:{} r:{:0.5f} g:{:0.5f} b{:0.5f}".format(i, rlux, glux, blux))
        f.write("{},{:0.5f},{:0.5f},{:0.5f}\n".format(i, rlux, glux, blux))
    
    f.close()

if __name__ == '__main__':
    sys.exit(main())
