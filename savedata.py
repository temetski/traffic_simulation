#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

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


#REAL_LANES = 4
#ROADLENGTH = 100
#TRIALS = 50

#AREA = 1 * (REAL_LANES) * ROADLENGTH
POS = 0
LANE = 1
SPEED = 2
SIZE = 3
LAST = -1


def throughput_norm(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SPEED]/ROADLENGTH*(vehicles[SIZE]/1000)
                     for vehicles in dist_trial[LAST]])


def throughput(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SPEED]/ROADLENGTH for vehicles in dist_trial[LAST]])

def efficiency(dist_trial):
    """Computes the efficiency of one trial of the simulation."""
    s = [vehicles[SPEED]/ROADLENGTH for vehicles in dist_trial[LAST]]
    throughput = np.sum(s)
    maxthroughput = 5*len(s)*1000/ROADLENGTH
    return throughput/maxthroughput


def throughput_car(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([ vehicles[SPEED]/ROADLENGTH if (vehicles[SIZE] == 4000) else 0 for vehicles in dist_trial[LAST] ])


def velocities(velo_trial):
    """Computes the average velocity of one trial of the simulation"""
    return np.average([vehicles[:,SPEED] for vehicles in velo_trial])


def lanechangecount(dist_trial):
    """Counts the number of lane changes per timestep
    of one trial of the simulation."""
    lanedat = dist_trial[:,:, LANE]
    diff = lanedat != np.roll(lanedat, 1, axis=0)
    return np.average(np.sum(diff, axis=0))


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
    RATIOS = [0, 0.25, 0.5, 0.75, 1]
    THROUGHPUT = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    THROUGHPUT_NORM = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    THROUGHPUT_CAR = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    VELOCITIES = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    LCCOUNT = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    EFFICIENCY = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    for x, ratio in enumerate(RATIOS):
        for y, density in enumerate(DENSITIES):
            try:
                data = load(ratio, density)
                np.savez_compressed("CarRatio.%.2f_Density.%.2f.npz" % (ratio, density), data=data)
                os.remove("CarRatio.%.2f_Density.%.2f.bz2" % (ratio, density))
            except:
                pass
            try:
                data = np.load("CarRatio.%.2f_Density.%.2f.npz" % (ratio, density))["data"]
                datasum = np.cumsum(data[:, :, :, :], axis=1)
                THROUGHPUT[x][y] = [throughput(trial)
                                    for trial in datasum]
                THROUGHPUT_NORM[x][y] = [throughput_norm(trial)
                                    for trial in datasum]
                THROUGHPUT_CAR[x][y] = [throughput_car(trial)
                                        for trial in datasum]
                LCCOUNT[x][y] = [lanechangecount(trial)
                                   for trial in data]
                VELOCITIES[x][y] = [velocities(trial) for trial in data]
                EFFICIENCY[x][y] = [efficiency(trial) for trial in datasum]
            except:
                print ratio, density
    np.savez_compressed("data.npz", THROUGHPUT=THROUGHPUT,
                                    THROUGHPUT_CAR=THROUGHPUT_CAR,
                                    LCCOUNT=LCCOUNT,
                                    VELOCITIES=VELOCITIES,
                                    THROUGHPUT_NORM=THROUGHPUT_NORM,
                                    EFFICIENCY=EFFICIENCY)
#    np.savez_compressed("efficiency.npz", EFFICIENCY=EFFICIENCY)
    print time.time()-to
