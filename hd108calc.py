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

    with open('hd108data_g0i0rg31gg31bg31_255_65535.txt', newline='\n') as csvfile:
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

    plt.plot(ra, color='salmon')
    plt.plot(ga, color='limegreen')
    plt.plot(ba, color='royalblue')

#    plt.plot(rq, color='darkred')
#    plt.plot(gq, color='forestgreen')
#    plt.plot(bq, color='darkblue')

#    plt.plot(ri, color='darkred')
#    plt.plot(gi, color='forestgreen')
#    plt.plot(bi, color='darkblue')

    plt.show()

if __name__ == '__main__':
    sys.exit(main())
