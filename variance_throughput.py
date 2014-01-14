# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import cPickle
import matplotlib.lines as lines
import matplotlib.pyplot as plt
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
    for t in xrange(TRIALS):
#                bzfile = bz2.BZ2File("CarRatio.%.2f_Density.%.2f.h5.bz2" % (ratio,density))
#                ucdata = bz2.decompress()
        fid = h5py.h5f.open("CarRatio.%.2f_Density.%.2f.h5" % (ratio,density))
        group = h5py.h5g.open(fid, "CarRatio::%.2f/Density::%.2f/" %
                                    (ratio, density))
        dset = h5py.h5d.open(group, "Trial::%04d" % (t+1))
        rdata = np.zeros(dset.shape)
        dset.read(h5py.h5s.ALL, h5py.h5s.ALL, rdata)
       # throughput.append(rdata)
        throughput = np.append(throughput, rdata)
    return throughput



fluxes = np.zeros([9,19])
variance = np.zeros([9,19, 2])
for x, ratio in enumerate(np.arange(0.1,1,0.1)):
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
plt.legend()
plt.xlabel('road density', size=18)
plt.ylabel('number of exiting vehicles', size=18)
plt.ylim(0,2000)
plt.xlim(0,1.2)
plt.title(r'Two Real lanes with adaptation', size=18)

plt.savefig("throughput.png")
