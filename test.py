# -*- coding: utf-8 -*-
"""
Created on Fri May 09 10:00:16 2014

@author: Damian
"""

import numpy as np
from subprocess import call
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import h5py
from load_params import ROADLENGTH, VIRTUAL_LANES, LANE_CHANGE_PROB
PATTERN = np.zeros([4, 2])
PATTERN[1:3, :] += 1
TOP = 0
BOTTOM = 3


def check_pattern(test):
    '''Assumes test is of shape (4,4)'''
    if ((test[:, 2:] == PATTERN).all() and
            ((test[TOP, :2] == [1, 1]).all()
            or (test[BOTTOM, :2] == [1, 1]).all())):
        return True
    else:
        return False


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


def road_create(vehicledata, ratio, density, lanes):
    timesteps = vehicledata.shape[0]
    road = np.zeros((timesteps, lanes, 100))
    for t, time in enumerate(vehicledata):
        for vehicle in time:
            pos = vehicle[0]
            lane = vehicle[1]
            size = vehicle[3]
            if size == 4:
                road[t, lane:lane+2, pos-1:pos+1] = 1
            else:
                road[t, lane, pos] = 2
    return road


def count_pattern(timestep_road):
    count = 0
    for i in xrange(1, ROADLENGTH+1):
        timestep_road = np.roll(timestep_road, i, axis=1)
        if check_pattern(timestep_road[:,:4]):
            count += 1
    return count


def main(ratio, density, lanes):
    vehicledata = load(ratio, density)
    road = road_create(vehicledata, ratio, density, lanes)
    count_arr = np.zeros(1000)
    for t, timestep_road in enumerate(road):
        count_arr[t] = count_pattern(timestep_road)
    #    for trial, trial_road in enumerate(road):
    #        for t, timestep_road in enumerate(trial_road):
    #            count_arr[t+trial] = count_pattern(timestep_road)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    y, x = np.histogram(count_arr, bins=np.max(count_arr), density=True)
    ax.hist(count_arr, bins=np.max(count_arr), normed=True, color="0.5")
    ax.set_xlabel("Pattern occurence per timestep")
    ax.set_xlim(min(x), max(x))
    plt.grid()
    #    ax_inset = fig.add_axes([0.622, 0.6, 0.25, 0.25])
    #    ax_inset.bar(x[:-1], np.cumsum(y), width=x[1]-x[0],
    #                 color='0.7', edgecolor='none')
    #    ax_inset.set_ylim(0, 1)
    #    ax_inset.set_xlim(min(x), max(x))
    #    ax_inset.set_title("CDF")
    #    plt.setp(ax_inset, xticks=[], yticks=[])
    #    ax.set_title(DIRNAME.replace("_", " ") + "\t$\kappa=%.2f$" % ratio)
    fig.savefig('pattern_CR.%.2f.D%.2f.pdf' % (ratio, density),
                bbox_inches='tight')
    plt.clf()
#    return 0


#if __name__ == "__main__":
#    import argparse
#    parser = argparse.ArgumentParser("Generates animated simlation")
#    parser.add_argument("--carratio", help="Specify car ratio", type=float)
#    parser.add_argument("--density", help="Specify density", type=float)
#    parser.add_argument("--lanes", help="Specify lanes", type=int)
#    args = parser.parse_args()
#    if (args.carratio is not None
#        and args.density is not None
#        and args.lanes is not None):
#        main(args.carratio, args.density, args.lanes)


ratio = 1
density = 0.2
lanes = 4
vehicledata = load(ratio, density)
road = road_create(vehicledata, ratio, density, lanes)
count_arr = np.zeros(1000)
for t, timestep_road in enumerate(road):
    count_arr[t] = count_pattern(timestep_road)
#    for trial, trial_road in enumerate(road):
#        for t, timestep_road in enumerate(trial_road):
#            count_arr[t+trial] = count_pattern(timestep_road)
fig = plt.figure(1)
ax = fig.add_subplot(111)
y, x = np.histogram(count_arr, bins=np.arange(max(count_arr)+2))
y_nonzero = y[1:]
x_nonzero = x[1:-1]
ynorm = 1.*y_nonzero/np.sum(y_nonzero)
ax.bar(x_nonzero, y_nonzero, width=x[1]-x[0],
             color='0.7')
#ax.hist(count_arr, bins=np.max(count_arr+1), normed=True, color="0.5")
ax.set_xlabel("Pattern occurence per timestep")
ax.set_xlim(min(x_nonzero), max(x))
#    ax_inset = fig.add_axes([0.622, 0.6, 0.25, 0.25])

#    ax_inset.set_ylim(0, 1)
#    ax_inset.set_xlim(min(x), max(x))
#    ax_inset.set_title("CDF")
#    plt.setp(ax_inset, xticks=[], yticks=[])
#    ax.set_title(DIRNAME.replace("_", " ") + "\t$\kappa=%.2f$" % ratio)
fig.savefig('pattern_CR.%.2f.D%.2f.V%s.LC%.1f.pdf' % 
            (ratio, density, VIRTUAL_LANES, LANE_CHANGE_PROB),
            bbox_inches='tight')
plt.clf()
#    return 0
