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

def v_dist(trial):
    """Computes the throughput of one trial of the simulation."""
    return [np.mean(time) for time in trial]


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
    
    RATIOS = [0,0.5,1]
    DENSITIES = [0.09,0.5,0.95]
    VDIST = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    VDIST_SPACE = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    for x, ratio in enumerate(RATIOS):
        for y, density in enumerate(DENSITIES):

            data = np.load("CarRatio.%.2f_Density.%.2f.npz" % (ratio, density))["data"]
            datasum = data[:, :, :, SPEED]
            VDIST = np.mean(datasum, axis=1)
            VDIST_SPACE = np.mean(datasum, axis=2)

            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            plt.grid()
            bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            ydata = VDIST.flatten()
            bin1 = (np.max(ydata)-np.min(ydata))/50
            weights = np.ones_like(ydata)/len(ydata)
            plt.hist(ydata, bins=50, color='b', alpha=0.7, label=r"$<v>_{time}$", weights=weights, edgecolor='b')

            ydata = VDIST_SPACE.flatten()
            weights = np.ones_like(ydata)/len(ydata)
            bin2 = (np.max(ydata)-np.min(ydata))/50
            ratiobin=bin2/bin1
            plt.hist(ydata, bins=50, color='0.5', alpha=0.8, label=r"$<v>_{space}$", weights=weights/ratiobin, edgecolor='0.5')
            ax.set_xlabel(r'Speed ($v$)')
            ax.set_ylabel('Probability')
            plt.legend(loc='best')

            fig.savefig('../distributions/vdist_stacked_%.1f_%.1f_%s.pdf' % (ratio,density,DIRNAME), bbox_inches='tight', dpi=300)
            ax.cla()

    data = np.load("CarRatio.%.2f_Density.%.2f.npz" % (0, 0.72))["data"]
    datasum = data[:, :, :, SPEED]
    VDIST = np.mean(datasum, axis=1)
    VDIST_SPACE = np.mean(datasum, axis=2)

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plt.grid()
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    ydata = VDIST.flatten()
    bin1 = (np.max(ydata)-np.min(ydata))/50
    weights = np.ones_like(ydata)/len(ydata)
    plt.hist(ydata, bins=50, color='b', alpha=0.7, label=r"$<v>_{time}$", weights=weights, edgecolor='b')

    ydata = VDIST_SPACE.flatten()
    weights = np.ones_like(ydata)/len(ydata)
    bin2 = (np.max(ydata)-np.min(ydata))/50
    ratiobin=bin2/bin1
    plt.hist(ydata, bins=50, color='0.5', alpha=0.8, label=r"$<v>_{space}$", weights=weights/ratiobin, edgecolor='0.5')
    ax.set_xlabel(r'Speed ($v$)')
    ax.set_ylabel('Probability')
    plt.legend(loc='best')

    fig.savefig('../distributions/vdist_stacked_%.1f_%.1f_%s.pdf' % (0,0.72,DIRNAME), bbox_inches='tight', dpi=300)
    ax.cla()
