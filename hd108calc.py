#!/usr/bin/env python3

import sys
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

ra = []
ga = []
ba = []

rq = []
gq = []
bq = []

def rfunc(x):
    return x

def gfunc(x):
    return -1.830981360906352 * np.exp(-0.790 * x) + 1.830981360906352

def bfunc(x):
    return -2.272202427870712 * np.exp(-0.580 * x) + 2.272202427870712

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
        gq.append(gfunc(i))

    for i in np.arange(0, 1, 1/256):
        bq.append(bfunc(i))


    plt.plot(ra, color='salmon', linestyle='dashed')
    plt.plot(ga, color='limegreen', linestyle='dashed')
    plt.plot(ba, color='royalblue', linestyle='dashed')

    plt.plot(rq, color='darkred')
    plt.plot(gq, color='forestgreen')
    plt.plot(bq, color='darkblue')

    plt.show()

if __name__ == '__main__':
    sys.exit(main())
