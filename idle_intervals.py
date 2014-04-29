#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Damian"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
#matplotlib.rcParams.update({'font.size': 15})
import matplotlib.pyplot as plt
import glob
import re
import os
from subprocess import call
import h5py


#REAL_LANES = 4
ROADLENGTH = 100
TRIALS = 50
TIMESTEPS = 1000

#AREA = 1 * (REAL_LANES) * ROADLENGTH
SPEED = -2
SIZE = -1
LAST = -1


def load(_ratio, _density):
    """Loads data from the hdf5 dataset."""
    vehicledata = np.array([], dtype=np.int8)
    filename = "CarRatio.%.2f_Density.%.2f.h5" % (_ratio, _density)
    call(['bunzip2', filename + '.bz2'])
    fid = h5py.File(filename, 'r')
    for n in xrange(TRIALS):
        group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
        _trial = "Trial::%04d" % (n + 1)
        dset = fid[group + _trial]
        vehicledata = np.append(vehicledata, dset)
    vehicledata = np.reshape(vehicledata, (TRIALS, dset.shape[0],
                                           dset.shape[1],
                                           dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return vehicledata


def count(vehicle, intervals):
    count = 0 
    for speed in vehicle:
        if speed == 0:
            count += 1
        else:
            intervals.append(count)
            count = 0
    return intervals

def main(ratio, density):
    DIRNAME = os.path.split(os.getcwd())[1]
    data = load(ratio, density)
    intervals = []
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for trial in data:
        for i in range(trial.shape[1]):
            intervals = count(trial[:, i, SPEED], intervals)
    y, x = np.histogram(intervals, bins=np.max(intervals), density=True)
    ax.hist(intervals, bins=np.max(intervals), normed=True, color="0.5", log=True)
    ax.set_xlabel("Non-moving intervals")
    ax.set_xlim(min(x), max(x))
    ax_inset = fig.add_axes([0.622, 0.6, 0.25, 0.25])
    ax_inset.bar(x[:-1], np.cumsum(y), width=x[1]-x[0],
                 color='0.7', edgecolor='none')
    ax_inset.set_ylim(0, 1)
    ax_inset.set_xlim(min(x), max(x))
    ax_inset.set_title("CDF")
#    plt.setp(ax_inset, xticks=[], yticks=[])
    ax.set_title(DIRNAME.replace("_", " ") + "\t$\gamma=%.2f$" % ratio)
    fig.savefig('stophist_CR.%.2f.D%.2f.png' % (ratio, density),
                bbox_inches='tight')
    plt.clf()
    plt.loglog(x[:-1], y)
    plt.savefig("test.png")
    

if __name__ == "__main__":
#    import argparse
#    parser = argparse.ArgumentParser("Generates animated simlation")
#    parser.add_argument("--carratio", help="Specify car ratio", type=float)
#    parser.add_argument("--density", help="Specify density", type=float)
#    args = parser.parse_args()
#    if (args.carratio != None and
#         args.density != None):
#        main(args.carratio, args.density)
#    else:
#        parser.print_help()

    ratios = [0,.25,.5,.75,1]
    densities = np.arange(0.75,1, 0.05)
    for i in ratios:
        for j in densities:
            main(i, j)

#    main(0, 0.5)
#    main(1, 0.95)
