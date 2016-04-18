#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import matplotlib
#matplotlib.use("Agg")
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import glob
import re
import os
from subprocess import call
import h5py


REAL_LANES = 4
ROADLENGTH = 50
TRIALS = 50
AREA = 1*(REAL_LANES)*ROADLENGTH
SPEED = 0
SIZE = -1
LAST = -1


def throughput(dist_trial):
    """Computes the throughput of one trial of the simulation."""
    return np.sum([vehicles[SPEED]/ROADLENGTH for vehicles in dist_trial[LAST]])


#def load(_ratio, _density):
#    '''Loads data from the hdf5 dataset.'''
#    vehicledata = np.array([], dtype=np.int8)
#    filename = "CarRatio.%.2f_Density.%.2f.h5" % (_ratio, _density)
#    call(['bunzip2', filename+'.bz2'])
#    fid = h5py.File(filename, 'r')
#    n = 1
#    group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
#    _trial = "Trial::%04d" % (n)
#    dset = fid[group+_trial]
#    vehicledata = np.append(vehicledata, dset)
#    vehicledata = np.reshape(vehicledata, (dset.shape[0],
#                                           dset.shape[1],
#                                           dset.shape[2]))
#    fid.close()
#    call(["bzip2", "-6", filename])
#    return vehicledata


def load(_ratio, _density):
    """Loads data from the hdf5 dataset."""
    vehicledata = np.array([], dtype=np.int8)
    filename = "CarRatio.%.2f_Density.%.2f.h5" % (_ratio, _density)
    call(['bunzip2', filename + '.bz2'])
    fid = h5py.File(filename, 'r')
    for n in xrange(1):
        group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
        _trial = "Trial::%04d" % (n + 1)
        dset = fid[group + _trial]
        vehicledata = np.append(vehicledata, dset)
    vehicledata = np.reshape(vehicledata, (dset.shape[0],
                                           dset.shape[1],
                                           dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return vehicledata


ratio = 0
density = 0.05
vehicledata = load(ratio, density)
carchoices = np.random.randint(vehicledata.shape[1], size=4)
fig = plt.figure()
timesteps = range(vehicledata.shape[0])
for i, vehicle in enumerate(carchoices):
    vel = vehicledata[:, vehicle, 0]
    ax = fig.add_subplot(carchoices.size, 1, i)
    ax.plot(range(1000), vel)
    ax.set_ylim(0, 5)
plt.show()
