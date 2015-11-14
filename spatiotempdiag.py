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
from load_params import VIRTUAL_LANES, REAL_LANES


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
            grid[i].set_title(r"$l_%s$" % i)
            grid[i].set_xticklabels([])
    else:
        fig = plt.figure(1)
        STD = road[:,0,:]
        grid = fig.add_subplot(111)
        grid.imshow(STD, cmap="binary", interpolation="nearest")
        grid.set_title(r"$l_%s$" % i)
        grid.set_xticklabels([])
    plt.savefig('CR.%.2f.D%.2f.V%s.pdf' % (ratio, density, VIRTUAL_LANES),
                bbox_inches="tight")


def main(ratio, density):
    lanes = REAL_LANES + VIRTUAL_LANES
    pos = 0
    lane = 1
    size = 3
    vehicledata = load(ratio, density)
    tempo_diagram(vehicledata, ratio, density, lanes)
'''    for t, timestep in enumerate(vehicledata[-100:]):
        fig = plt.figure(figsize=(10, 0.2*lanes), dpi=150)
        ax = fig.add_subplot(111, axis_bgcolor='gray')
        cars = np.array([[i[pos], i[lane], 0] for i in timestep if i[size] == 4])
        motorcycles = np.array([[i[pos], i[lane], 0] for i in timestep if i[size] == 1])
        if cars.size:
            carplot(ax, cars, lanes)
        if motorcycles.size:
            motoplot(ax, motorcycles, lanes)
        fig.savefig("%s" % t, dpi=150)
        ax.cla()
        plt.close(fig)
    call("avconv -f image2 -i %d.pdf -r 5 -vcodec libx264 -b 800k out.mp4", shell=True)
    call("rm [0-9]*.pdf", shell=True)
    return 0'''


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generates animated simlation")
    parser.add_argument("--carratio", help="Specify car ratio", type=float)
    parser.add_argument("--density", help="Specify density", type=float)
    args = parser.parse_args()
    if (args.carratio != None and
         args.density != None):
        main(args.carratio, args.density)
    else:
        parser.print_help()
