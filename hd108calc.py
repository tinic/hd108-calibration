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

def func(x, a, b, c):
    return a * np.exp(b * x) + c

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
        rq.append(func(i, -1.83, -0.79, 1.83))

    plt.plot(ra, color='red')
    plt.plot(ga, color='green')
    plt.plot(ba, color='blue')

    plt.plot(rq, color='black')

    plt.show()

if __name__ == '__main__':
    sys.exit(main())
