#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 2 00:18:38 2015

@author: Damian
"""
from __future__ import division
import numpy as np
import matplotlib
from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
                        VIRTUAL_LANES, SLOWDOWN, LANE_CHANGE_PROB
matplotlib.use("Agg")
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams.update({'axes.labelsize': 17})
import matplotlib.pyplot as plt
import glob
import re
import os
from subprocess import call
import h5py

POS = 0
LANE = 1
SPEED = 2
SIZE = 3
PSLOW = 4
LAST = -1



def randcount_all(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    decsum = 0
    for time in xrange(len(dist_trial)-1):
        decsum += np.sum((dist_trial[time,:,SPEED] < dist_trial[time-1,:,SPEED])*(0==dist_trial[time,:,PSLOW]))
        # for nveh in xrange(len(dist_trial[time])):
        #     vehicle = dist_trial[time+1][nveh]
        #     vehicle_past = dist_trial[time][nveh]
        #     if vehicle_past[SPEED] > vehicle[SPEED]:
        #         decsum += 1
    return decsum/len(dist_trial[0,:])/time



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


if __name__ == "__main__":
    import time
    to = time.time()
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1.,0.01)
    RATIOS = np.array([])
    FILES = glob.glob("CarRatio*.npz")
    for i in FILES:
        car_ratio = float(re.findall(r"CarRatio.(\d.\d+)", i)[0])
        if car_ratio not in RATIOS and car_ratio in __plot_ratios__:
            RATIOS = np.append(RATIOS, car_ratio)
    RATIOS.sort()
    COLLISION = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    for x, ratio in enumerate(RATIOS):
        for y, density in enumerate(DENSITIES):
            data = np.load("CarRatio.%.2f_Density.%.2f.npz" % (ratio, density))["data"]
            COLLISION[x][y] = [randcount_all(trial)
                                for trial in data]

    np.savez_compressed("collision.npz", COLLISION=COLLISION)
    print time.time()-to
