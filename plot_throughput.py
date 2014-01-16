#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import cPickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.lines as lines
import matplotlib.pyplot as plt
from subprocess import call
import h5py


REAL_LANES = 4
ROADLENGTH = 50
TRIALS = 50

area = 1*(REAL_LANES)*ROADLENGTH
speed = 0
size = -1
last = -1

def throughputnorm(trial, sizes):
    x= [vehicles[speed]/ROADLENGTH for vehicles in trial[-1]]
    return 1.*np.sum(x)/len(x)

def throughput(trial, sizes):
    return np.sum([vehicles[speed]/ROADLENGTH for vehicles, s in zip(trial[last],
                   sizes[last]) if s])
def through(vehicles):
    return 1.*np.sum(i[0] for i in vehicles)/ROADLENGTH/len(vehicles)

def load(ratio, density):
    throughput = np.array([], dtype=np.int8)
    filename = "CarRatio.%.2f_Density.%.2f.h5" % (ratio,density)
    call(['bunzip2', filename+'.bz2'])
    fid = h5py.File(filename, 'r')
    for t in xrange(TRIALS):
        group = "CarRatio::%.2f/Density::%.2f/" % (ratio, density)
        trial = "Trial::%04d" % (t+1)
        dset = fid[group+trial]
        throughput = np.append(throughput, dset)

    throughput = np.reshape(throughput, (TRIALS, dset.shape[0],
                                         dset.shape[1],
                                         dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return throughput



fluxes = np.zeros([1,19])
variance = np.zeros([1,19, 2])
for x, ratio in enumerate(np.arange(1)):#0.1,1,0.1)):
    if ratio == 1:
        ratio = 1
    if ratio == 0:
        ratio = 0
    for y, density in enumerate(np.arange(0.05,1,0.05)):
        vehicledata = load(ratio, density)
        sizedata = vehicledata[:,2001:,:,size]
        vehicledata = np.cumsum(vehicledata[:,2001:,:,:], axis=1)
        vehicleflux = [throughput(trial,sizes)
                        for trial, sizes in zip(vehicledata, sizedata)]
        fluxes[x,y] = np.mean(vehicleflux)
        variance[x,y] = [np.max(vehicleflux), np.min(vehicleflux)]


markers = list(lines.Line2D.markers.keys())
markers.sort()
N = len(markers)
labels = np.arange(0.1, 1, 0.1)
for ydata, label, i in zip(fluxes, labels, range(len(labels))):
    marker = markers[i%N]
#    plt.plot(np.arange(0.05,1,0.05), ydata, label=label, marker=marker)
    plt.errorbar(np.arange(0.05,1,0.05), ydata, yerr=np.abs(variance[i].T-ydata),label=label, marker=marker)
#plt.legend(loc="upper left", bbox_to_anchor=(1,1))
#plt.legend()
plt.xlabel('road density', size=18)
plt.ylabel('number of exiting vehicles', size=18)
#plt.ylim(0,2000)
#plt.xlim(0,1.2)
plt.title(r'Two Real lanes with adaptation', size=18)

plt.savefig("throughput.png")
