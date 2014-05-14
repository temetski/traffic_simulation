#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import matplotlib
from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
                        VIRTUAL_LANES, SLOWDOWN
LANE_CHANGE_PROB = 0.8
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

#AREA = 1 * (REAL_LANES) * ROADLENGTH
SPEED = -2
SIZE = -1
LAST = -1


def throughput(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SPEED]/ROADLENGTH for vehicles in dist_trial[LAST]])


def velocities(velo_trial):
    """Computes the average velocity of one trial of the simulation"""
    return np.average([vehicles[:,SPEED] for vehicles in velo_trial])


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
    DENSITIES = np.arange(0.05, 1, 0.05)
    RATIOS = np.array([])
    for i in FILES:
        car_ratio = float(re.findall(r"CarRatio.(\d.\d+)", i)[0])
        if car_ratio not in RATIOS and car_ratio in __plot_ratios__:
            RATIOS = np.append(RATIOS, car_ratio)
    RATIOS.sort()
    THROUGHPUT = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    VELOCITIES = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
    for x, ratio in enumerate(RATIOS):
        for y, density in enumerate(DENSITIES):
            data = load(ratio, density)
            datasum = np.cumsum(data[:, :, :, :], axis=1)
            flux = [throughput(trial)
                    for trial in datasum]
            THROUGHPUT[x][y] = flux
            VELOCITIES[x][y] = [velocities(trial) for trial in data]
    MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, median, label, i in zip(THROUGHPUT, MEDIANS, RATIOS, range(len(RATIOS))):
        color = "%s" % (i*0.15)
        ax.plot(DENSITIES, median, color=color, linewidth=3,
                label=r"$\gamma = %.2f$" % label)
        bp = ax.boxplot(ydata, positions=DENSITIES, widths=0.02)
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['fliers'], color=color)
        plt.setp(bp['medians'], color=color)
        plt.legend()
    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $l_v = %d$" % 
            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Throughput')
    ax.set_ylim(0, 2000)
    ax.set_xlim(0, 1)
    ax.set_xticks(DENSITIES[1::2])
    plt.grid()
    fig.savefig('throughput_%s.png' % DIRNAME, bbox_inches='tight', dpi=300)
    ax.cla()


    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    for ydata, median, label, i in zip(VELOCITIES, MEDIANS, RATIOS, range(len(RATIOS))):
        color = "%s" % (i*0.15)
        ax2.plot(DENSITIES, np.median(ydata, axis=1), 
                 color=color, linewidth=3,
                 label=r"$\gamma = %.2f$" % label)
        bp = ax2.boxplot(ydata, positions=DENSITIES, widths=0.02)
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['fliers'], color=color)
        plt.setp(bp['medians'], color=color)
        plt.legend()
    ax2.set_xlabel('road density')
    ax2.set_ylabel('median average velocity')
    ax2.set_xlim(0, 1)
    ax2.set_xticks(DENSITIES[1::2])
    plt.grid()
    fig2.savefig('velocities_%s.png' % DIRNAME, bbox_inches='tight', dpi=300)
    ax2.cla()
