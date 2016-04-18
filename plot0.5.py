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
matplotlib.rcParams.update({'axes.labelsize': 17,'legend.fontsize': 15})
import matplotlib.pyplot as plt
#plt.rc('font',family='serif')
plt.rc('font',serif='Helvetica')
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


def plot():
    color = "%s" % (i*0.18)
    median = np.median(ydata, axis=1)
    errminus = median - np.percentile(ydata,25, axis=1)
    errplus = np.percentile(ydata,75, axis=1) - median
    ax.errorbar(DENSITIES, median, [errminus, errplus], markeredgecolor='black',  color=color, markersize=6,markeredgewidth=0.2,
                linewidth=2, elinewidth=1, label=r"$\kappa = %.2f$" % label,
                marker=marks[i%2],dashes=ls[i%2])
    plt.legend()



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
    FILES = glob.glob("CarRatio*")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    RATIOS = np.array(__plot_ratios__)
    all_data = np.load("data2.npz")
    THROUGHPUT = all_data["THROUGHPUT"]
    ls = [(), (13,3)]
    marks = ['o', 's']


    MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, label, i in zip(THROUGHPUT, RATIOS, range(len(RATIOS))):
        plot()
    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
            (LANE_CHANGE_PROB),  ha="left", va="top",
            size=20, bbox=bbox_props, transform=ax.transAxes)
    if VIRTUAL_LANES:
        ylim = 2800
    else:
        ylim = 2400
    ax.set_xlabel(r'Vehicle density ($\rho$)')
    ax.set_ylabel('Throughput ($Q$)')
    ax.set_ylim(0, ylim)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/throughput_%s.pdf' % DIRNAME, bbox_inches='tight', dpi=300)
    ax.cla()
