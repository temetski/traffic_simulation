#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
#import cPickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import glob
import re
from subprocess import call
import h5py


REAL_LANES = 4
ROADLENGTH = 50
TRIALS = 50

AREA = 1*(REAL_LANES)*ROADLENGTH
SPEED = 0
SIZE = -1
LAST = -1

def throughput(_trial):
    '''Computes the throughput of one trial of the simulation.'''
    return np.sum([vehicles[SPEED]/ROADLENGTH for vehicles in _trial[LAST]])

def load(_ratio, _density):
    '''Loads data from the hdf5 dataset.'''
    vehicledata = np.array([], dtype=np.int8)
    filename = "CarRatio.%.2f_Density.%.2f.h5" % (_ratio, _density)
    call(['bunzip2', filename+'.bz2'])
    fid = h5py.File(filename, 'r')
    for n in xrange(TRIALS):
        group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
        _trial = "Trial::%04d" % (n+1)
        dset = fid[group+_trial]
        vehicledata = np.append(vehicledata, dset)
    vehicledata = np.reshape(vehicledata, (TRIALS, dset.shape[0],
                                         dset.shape[1],
                                         dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return vehicledata

if __name__ == "__main__":
    FILES = glob.glob("*.bz2")
    DENSITIES = np.arange(0.05, 1, 0.05)
    RATIOS = np.array([])
    for i in FILES:
        car_ratio = float(re.findall(r"CarRatio.(\d.\d+)", i)[0])
        if car_ratio not in RATIOS:
            RATIOS = np.append(RATIOS, car_ratio)

    THROUGHPUT = np.zeros([len(RATIOS), len(DENSITIES)])
    STDEV = np.zeros([len(RATIOS), len(DENSITIES)])
    for x, ratio in enumerate(np.arange(1)):#0.1,1,0.1)):
        for y, density in enumerate(DENSITIES):
            data = load(ratio, density)
            # sizedata = vehicledata[:,2001:,:,SIZE]
            data = np.cumsum(data[:, :, :, :], axis=1)
            flux = [throughput(trial)
                            for trial in data]
            THROUGHPUT[x, y] = np.mean(flux)
            STDEV[x, y] = np.std(flux)

    __markers__ = list(lines.Line2D.markers.keys())
    __markers__.sort()
    N = len(__markers__)
    __labels__ = np.arange(0.1, 1, 0.1)
    for ydata, label, i in zip(THROUGHPUT, __labels__, range(len(__labels__))):
        marker = __markers__[i % N]
        plt.errorbar(DENSITIES, ydata, 
                    yerr=STDEV[i, :], label=label, marker=marker)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.xlabel('road density', size=18)
    plt.ylabel('number of exiting vehicles', size=18)
    #plt.ylim(0,2000)
    #plt.xlim(0,1.2)
    plt.title(r'Two Real lanes with adaptation', size=18)

    plt.savefig("throughput.png")
