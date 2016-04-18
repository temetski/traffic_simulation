# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 15:25:30 2014

@author: damian

Gets the average empty space for consecutive timesteps. Uses an or operator.
"""

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image
from subprocess import call
import os
import h5py
from load_params import VIRTUAL_LANES, REAL_LANES, TRIALS


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

def ave_empty(vehicledata, ratio, density, lanes):
    timesteps = vehicledata.shape[1]
    trials = vehicledata.shape[0]
    empty = []
    for tr in range(trials):
        road = np.zeros((timesteps, lanes, 100), dtype=bool)
        for t, time in enumerate(vehicledata[tr]):
            for vehicle in time:
                pos = vehicle[0]
                lane = vehicle[1]
                size = vehicle[3]
                if size == 4:
    	            road[t, lane:lane+2, pos-1:pos+1] = 1
                else:
    	            road[t, lane, pos] = 1
        ave = []
        for time in range(len(road)-1):
            rsum = road[time+1] + road[time]
            ave.append(np.sum(rsum==False))
        empty.append(np.mean(ave))
#    plt.plot(empty)
    return empty


#def main(ratio, density):
#



if __name__ == "__main__":
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
    __p_lambdas__ = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = [0.25]+[0.3]+[0.35]*5+[0.4]+[0.35]*2
    lanes = 5
    emp_space = []
    for ratio in [0.75]:
        for density, p_lambda in zip(DENSITIES, __p_lambdas__):
            os.chdir("lanechange_%.1f_virt_1" % p_lambda)
            vehicledata = load(ratio, density)
            emp_space.append(ave_empty(vehicledata, ratio, density, lanes))
            os.chdir('..')