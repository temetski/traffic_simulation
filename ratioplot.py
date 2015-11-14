#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 13:31:26 2014

@author: Damian
"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({'axes.labelsize': 17})
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image
from subprocess import call
import h5py
import sys


def load(_ratio, _density):
    '''Loads data from the hdf5 dataset.'''
    vehicledata = np.array([], dtype=np.int8)
    filename = "CarRatio.%.2f_Density.%.2f.h5" % (_ratio, _density)
    call(['bunzip2', filename + '.bz2'])
    fid = h5py.File(filename, 'r')
    group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
    _trial = "Trial::%04d" % (20)
    dset = fid[group+_trial]
    vehicledata = np.append(vehicledata, dset)
    vehicledata = np.reshape(vehicledata, (dset.shape[0],
                                           dset.shape[1],
                                           dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return vehicledata


def tempo_diagram(vehicledata, ratio, density, lanes):
    timesteps = vehicledata.shape[0]
    road = np.zeros((timesteps, lanes, 100), dtype=bool)
    for t, time in enumerate(vehicledata):
        for vehicle in time:
            pos = vehicle[0]
            lane = vehicle[1]
            size = vehicle[3]
            if size == 4:
	            road[t, lane:lane+2, pos-1:pos+1] = 1
            else:
	            road[t, lane, pos] = 1
    if lanes>1:
        fig = plt.figure(1)
        grid = ImageGrid(fig, 111,
                    nrows_ncols = (1, lanes), 
                    axes_pad=0.1,
                    )
        for i in range(lanes):
            STD = road[:,i,:]
            grid[i].imshow(STD, cmap="binary", interpolation="nearest")
            grid[i].set_title(r"$L_%s$" % i)
            grid[i].set_xticklabels([])
    else:
        fig = plt.figure(1)
        STD = road[:,0,:]
        grid = fig.add_subplot(111)
        grid.imshow(STD, cmap="binary", interpolation="nearest")
        grid.set_title(r"$L_%s$" % i)
        grid.set_xticklabels([])
    plt.savefig('CR.%.2f.D%.2f.pdf' % (ratio, density), bbox_inches="tight")


def plot(med1, med2):
    os.chdir(med1)
    from load_params import VIRTUAL_LANES, LANE_CHANGE_PROB
    os.chdir('..')
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    RATIOS = np.array([0, 0.25, 0.5, 0.75, 1])
    ls = [(), (15,2), "-", "--"]
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    med1dat = np.median(np.load(med1+filename)['THROUGHPUT'], axis=2)
    std1dat = np.std(np.load(med1+filename)['THROUGHPUT'], axis=2)
    med2dat = np.median(np.load(med2+filename)['THROUGHPUT'], axis=2)
    std2dat = np.std(np.load(med1+filename)['THROUGHPUT'], axis=2)
    ratio = med1dat/med2dat
    stdratio = np.sqrt((std1dat/med1dat)**2 + (std2dat/med2dat)**2)
    for median, label, i in zip(ratio, RATIOS, range(len(RATIOS))):
        color = "%s" % (i*0.15)
#        ax.plot(DENSITIES, median, color=color, linewidth=3,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])
        ax.errorbar(DENSITIES, median, color=color, linewidth=2,
                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2],
                yerr=median*stdratio[i])

    plt.legend(loc=2)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Ratio of throughput')
    ax.text(0.98, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" %
            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="right", va="top",
            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    if med2 == base:
        fig.savefig('images/ratio_%s.pdf' % med1, bbox_inches='tight', dpi=300)
    else:
        fig.savefig('images/ratio_%s%s.pdf' % (med1, med2),
                    bbox_inches='tight', dpi=300)
    ax.cla()
    del sys.modules['load_params']

def plot2(med1, med2):
    os.chdir(med1)
    from load_params import VIRTUAL_LANES, LANE_CHANGE_PROB
    os.chdir('..')
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    RATIOS = np.array([0, 0.25, 0.5, 0.75, 1])
    ls = [(), (15,2), "-", "--"]
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    med1dat = np.median(np.load(med1+filename)['THROUGHPUT'], axis=2)
    std1dat = np.std(np.load(med1+filename)['THROUGHPUT'], axis=2)
    med2dat = np.median(np.load(med2+filename)['THROUGHPUT'], axis=2)
    std2dat = np.std(np.load(med1+filename)['THROUGHPUT'], axis=2)
    ratio = med1dat/med2dat
    stdratio = np.sqrt((std1dat/med1dat)**2 + (std2dat/med2dat)**2)
    for median, label, i in zip(ratio, RATIOS, range(len(RATIOS))):
        color = "%s" % (i*0.15)
#        ax.plot(DENSITIES, median, color=color, linewidth=3,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])
        ax.errorbar(DENSITIES, median, color=color, linewidth=2,
                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2],
                yerr=median*stdratio[i])
    plt.plot(DENSITIES, [1.25]*len(DENSITIES), color='r', linewidth=2, linestyle='--')
    plt.legend(loc=2)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Ratio of throughput')
    ax.text(0.98, 0.97, r"$p_{\lambda} = %.2f$" %
            (LANE_CHANGE_PROB),  ha="right", va="top",
            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    if med2 == base:
        fig.savefig('images/ratio_%s.pdf' % med1, bbox_inches='tight', dpi=300)
    else:
        fig.savefig('images/ratio_%s%s.pdf' % (med1, med2),
                    bbox_inches='tight', dpi=300)
    ax.cla()
    del sys.modules['load_params']


if __name__ == "__main__":
    filename = "/data.npz"
    import glob
    import os
    folders = glob.glob("lanechange_*")
    base = "lanechange_0.0_virt_0"
#    for i in folders:
#        if not i == base:
#            plot(i, base)
#    plot(folders[2], folders[1])
    plot2('lanechange_1.0_virt_1', 'lanechange_1.0_virt_0')

