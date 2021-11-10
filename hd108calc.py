#!/usr/bin/env python3

import sys
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

# best match so far
gconst = 0.760
bconst = 0.550

ra = []
ga = []
ba = []

rq = []
gq = []
bq = []

ri = []
gi = []
bi = []

rc = []
gc = []
bc = []

'''
-a * exp(-b * 1) + a = 1

(1 - a) / - a = e ^ (-b)

-log((1-a)/(-a)) = b

a * (-exp(-b) + 1) = 1

1 / (-exp(-b) + 1)
'''

def rfunc(x):
    return x

def rifunc(x):
    return x

def gfunc(x, b):
    a = 1.0 / (-np.exp(-b) + 1.0)
    return -a * np.exp(-b * x) + a

def gifunc(x, b):
    a = 1.0 / (-np.exp(-b) + 1.0)
    return np.log((x - a) / -a) / -b

def bfunc(x, b):
    a = 1.0 / (-np.exp(-b) + 1.0)
    return -a * np.exp(-b * x) + a

def bifunc(x, b):
    a = 1.0 / (-np.exp(-b) + 1.0)
    return np.log((x - a) / -a) / -b

def main():

    with open('hd108data_g2i0rg31gg31bg31_0-1023.txt', newline='\n') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            ra.append(float(row[1]))
            ga.append(float(row[2]))
            ba.append(float(row[3]))

    rmax = max(ra)
    gmax = max(ga)
    bmax = max(ba)

    for i in range(len(ra)):
        ra[i] /= rmax;
    for i in range(len(ga)):
        ga[i] /= gmax;
    for i in range(len(ba)):
        ba[i] /= bmax;

    for i in np.arange(0, 1, 1/256):
        rq.append(rfunc(i))

    for i in np.arange(0, 1, 1/256):
        gq.append(gfunc(i, gconst))

    for i in np.arange(0, 1, 1/256):
        bq.append(bfunc(i, bconst))

    for i in np.arange(0, 1, 1/256):
        ri.append(rifunc(i))

    for i in np.arange(0, 1, 1/256):
        gi.append(gifunc(i, gconst))

    for i in np.arange(0, 1, 1/256):
        bi.append(bifunc(i, bconst))

    rc = ra.copy()
    gc = ga.copy()
    bc = ba.copy()

    # this correction map makes sure that
    # the response curve is monotone
    monotone_map = [
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
        0x0F, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15,
        0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D
    ]

    for i in range(len(ra)):
        rc[i] = ra[monotone_map[(i&0x1F)]+(i&(~0x1F))]
        gc[i] = ga[monotone_map[(i&0x1F)]+(i&(~0x1F))]
        bc[i] = ba[monotone_map[(i&0x1F)]+(i&(~0x1F))]

    plt.grid(True,'both','both')
    plt.xticks(np.arange(-1, 1023, step=16))

#    plt.plot(ra, color='salmon')
#    plt.plot(ga, color='limegreen')
#    plt.plot(ba, color='royalblue')

    plt.plot(rc, color='darkred')
    plt.plot(gc, color='forestgreen')
    plt.plot(bc, color='darkblue')

#    plt.plot(rq, color='darkred')
#    plt.plot(gq, color='forestgreen')
#    plt.plot(bq, color='darkblue')

#    plt.plot(ri, color='darkred')
#    plt.plot(gi, color='forestgreen')
#    plt.plot(bi, color='darkblue')

    plt.show()

if __name__ == '__main__':
    sys.exit(main())
