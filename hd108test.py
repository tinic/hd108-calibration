#!/usr/bin/env python3

import sys
import time
import board
import busio
import spidev
import math

# best match so far
r_const = 1.000
g_const = 0.760
b_const = 0.550

spi = spidev.SpiDev()

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

def main():
    spi.open(0,0)
    spi.bits_per_word = 8
    spi.max_speed_hz = 4000000

    # precompute constants
    ga_const =  math.exp(-g_const) - 1.0
    gai_const = + 1.0 / ga_const
    gbi_const = - 1.0 / g_const

    ba_const =  math.exp(-b_const) - 1.0
    bai_const = + 1.0 / ba_const
    bbi_const = - 1.0 / b_const

    t = 0
    while True:
        v = math.sin(t) * 0.5 + 0.5

        # correct output
        r = int(v * 65535.0)
        g = int((math.log((v + gai_const) * ga_const) * gbi_const) * 65535.0)
        b = int((math.log((v + bai_const) * ba_const) * bbi_const) * 65535.0)

        spi.writebytes2(leddat(r, g, b, 31, 31, 31))

        t += 0.001

if __name__ == '__main__':
    sys.exit(main())
