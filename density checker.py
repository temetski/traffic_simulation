#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
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
ROADLENGTH = 100
TRIALS = 50

AREA = 1. * (REAL_LANES+VIRTUAL_LANES) * ROADLENGTH
SPEED = -2
SIZE = -1
LAST = -1
LANE = 1

def throughput_norm(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SPEED]/ROADLENGTH*(vehicles[SIZE]/1000)
                     for vehicles in dist_trial[LAST]])


def throughput(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SIZE] for vehicles in dist_trial[LAST]])/AREA



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
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
    FILES = glob.glob("*.bz2")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1.,0.01)
    RATIOS = np.array([])
    for i in FILES:
        car_ratio = float(re.findall(r"CarRatio.(\d.\d+)", i)[0])
        if car_ratio not in RATIOS and car_ratio in __plot_ratios__:
            RATIOS = np.append(RATIOS, car_ratio)
    RATIOS.sort()
    THROUGHPUT = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]

    for x, ratio in enumerate(RATIOS):
        for y, density in enumerate(DENSITIES):
            data = load(ratio, density)
            datasum = np.cumsum(data[:, :, :, :], axis=1)
            THROUGHPUT[x][y] = [throughput(trial)
                                for trial in datasum]


