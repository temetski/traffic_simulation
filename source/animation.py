#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 13:31:26 2014

@author: Damian
"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rc("figure", dpi=150)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image
from subprocess import call
import h5py


def plotter(ax, array, lanes):
    line, = ax.plot(array[:, 0], array[:, 1]+0.45, 'o')
    ax.set_ylim(0, lanes)
    plt.gca().invert_yaxis()
    ax.set_xlim(0, 50)
    ax.hlines([2, 4], 0, 50, color='yellow', linestyles='dashed', linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return line


def motoplot(ax, array, lanes):
    size = 30, 30
    im = Image.open('Moto.png')
    im.thumbnail(size)
    im_w = im.size[0]
    im_h = im.size[1]
    line = plotter(ax, array, lanes)
    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255
    line._transform_path()
    path, affine = line._transformed_path.get_transformed_points_and_affine()
    path = affine.transform_path(path)
    for pixelPoint in path.vertices:
        # place image at point, centering it
        x0 = pixelPoint[0]-im_w/2
        y0 = pixelPoint[1]-im_h/2
        plt.figimage(im, x0, y0, zorder=100, origin='lower')


def carplot(ax, array, lanes):
    size = 44, 44
    vel = 2
    im = [Image.open('Car%s.png' % i) for i in range(6)]
    for i in range(6):
        im[i].thumbnail(size)
    im_w = im[0].size[0]
    im_h = im[0].size[1]
    line = plotter(ax, array, lanes)
    # We need a float array between 0-1, rather than
    # a uint8 array between 0-255
    line._transform_path()
    path, affine = line._transformed_path.get_transformed_points_and_affine()
    path = affine.transform_path(path)
    for i, pixelPoint in enumerate(path.vertices):
        velocity = array[i, vel]
        # place image at point, centering it
        x0 = pixelPoint[0]-3.*im_w/4
        y0 = pixelPoint[1]-3.*im_h/4
        plt.figimage(im[velocity], x0, y0, zorder=100, origin='lower')


def load(_ratio, _density):
    '''Loads data from the hdf5 dataset.'''
    vehicledata = np.array([], dtype=np.int8)
    filename = "Animation_CR.%.2f_D.%.2f.h5" % (_ratio, _density)
    call(['bunzip2', filename + '.bz2'])
    fid = h5py.File(filename, 'r')
    group = "CarRatio::%.2f/Density::%.2f/" % (_ratio, _density)
    _trial = "Trial::%04d" % (0)
    dset = fid[group+_trial]
    vehicledata = np.append(vehicledata, dset)
    vehicledata = np.reshape(vehicledata, (dset.shape[0],
                                           dset.shape[1],
                                           dset.shape[2]))
    fid.close()
    call(["bzip2", "-6", filename])
    return vehicledata


def tempo_diagram(vehicledata, lanes):
    timesteps = vehicledata.shape[0]
    road = np.zeros((timesteps, lanes, 50), dtype=bool)
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
            grid[i].set_title("Lane %s" % i)
    else:
        fig = plt.figure(1)
        STD = road[:,0,:]
        grid = fig.add_subplot(111)
        grid.imshow(STD, cmap="binary", interpolation="nearest")
        grid.set_title("Lane %s" % 0)
    plt.savefig('test.png', bbox_inches="tight")


def main(ratio, density, lanes):
    pos = 0
    lane = 1
    size = 3
    vehicledata = load(ratio, density)
#    tempo_diagram(vehicledata, lanes)
    # for t, timestep in enumerate(vehicledata[-100:]):
    #     fig = plt.figure(figsize=(10, 0.2*lanes), dpi=150)
    #     ax = fig.add_subplot(111, axis_bgcolor='gray')
    #     cars = np.array([[i[pos], i[lane], 0] for i in timestep if i[size] == 4])
    #     motorcycles = np.array([[i[pos], i[lane], 0] for i in timestep if i[size] == 1])
    #     if cars.size:
    #         carplot(ax, cars, lanes)
    #     if motorcycles.size:
    #         motoplot(ax, motorcycles, lanes)
    #     fig.savefig("%s" % t, dpi=150)
    #     ax.cla()
    #     plt.close(fig)
    # call("avconv -f image2 -i %d.png -r 5 -vcodec libx264 -b 800k ../out.mp4", shell=True)
    call("rm [0-9]*.png", shell=True)
    call("rm Animation_*", shell=True)
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generates animated simlation")
    parser.add_argument("--carratio", help="Specify car ratio", type=float)
    parser.add_argument("--density", help="Specify density", type=float)
    parser.add_argument("--lanes", help="Specify lanes", type=int)
    args = parser.parse_args()
    if (args.carratio != None and
         args.density != None and
         args.lanes != None):
        main(args.carratio, args.density, args.lanes)
    else:
        parser.print_help()
