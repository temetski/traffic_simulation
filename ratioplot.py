#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 13:31:26 2014

@author: Damian
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image
from subprocess import call
import h5py



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
    plt.savefig('CR.%.2f.D%.2f.png' % (ratio, density), bbox_inches="tight")


def plot(med1, med2):
    DENSITIES = np.arange(0.05, 1, 0.05)
    RATIOS = np.array([0, 0.25, 0.5, 0.75, 1])
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    med1dat = np.load(med1+filename)['medians']
    med2dat = np.load(med2+filename)['medians']
    ratio = med1dat/med2dat
    for median, label, i in zip(ratio, RATIOS, range(len(RATIOS))):
        color = "%s" % (i*0.15)
        ax.plot(DENSITIES, median, color=color, linewidth=3,
                label=r"$\gamma = %.2f$" % label)
    plt.legend(loc=2)
    ax.set_xlabel('road density')
    ax.set_ylabel('number of exiting vehicles')
#    ax.set_ylim(0, 2000)
    ax.set_title((med1 + med2).replace("_", " "))
    ax.set_xlim(0, 1)
    ax.set_xticks(DENSITIES[1::2])
    plt.grid()
    fig.savefig('ratiothroughput_%s.png' % (med1[:-1] + med2[:-1]), bbox_inches='tight', dpi=300)
    ax.cla()


if __name__ == "__main__":
    real = "Two_Real/"
    realno = real[:-1]+"_NoLaneChange/"
    virt = "Two_Car_Lanes_Virtual/"
    filename = "median_dat.npz"
    plot(realno, real)
    plot(realno, virt)
    plot(real, virt)

