# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:42:42 2013

@author: Damian
"""

#import cPickle
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from subprocess import call
import h5py


#all_ = open('ratiovehicles 4lanes.dat', 'rb')
#cars = open('ratiovehicles 4lanes cars.dat', 'rb')
#motorcycles = open('ratiovehicles 4lanes motorcycles.dat', 'rb')
#files = [all_, cars, motorcycles]

SPEED = -2
SIZE = -1
TRIALS = 50

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


def movement(timestep):
    vel = [vehicle[SPEED] for vehicle in timestep if vehicle[SIZE]!=1]
    if len(vel)==0:
        return 0
    return (1.0*(np.count_nonzero(vel))/len(vel))
    
ls = [(), (15,2), "-", "--"]
RATIOS = [0,.25,.5,.75,1]
DENSITIES = np.arange(0.05,1, 0.05)
MOVEMENT = [[None for i in range(len(DENSITIES))]
                  for j in range(len(RATIOS))]
for x, ratio in enumerate(RATIOS):
    for y, density in enumerate(DENSITIES):
        data = load(ratio, density)
        flux = [[movement(timestep) for timestep in trial] 
                        for trial in data]
        MOVEMENT[x][y] = np.average(flux, axis=1)
MEDIANS = np.median(MOVEMENT, axis=2)
fig = plt.figure(1)
ax = fig.add_subplot(111)
for ydata, median, label, i in zip(MOVEMENT, MEDIANS, RATIOS, range(len(RATIOS))):
    color = "%s" % (i*0.15)
    ax.plot(DENSITIES, median, color=color, linewidth=3,
            label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])
    bp = ax.boxplot(ydata, positions=DENSITIES, widths=0.02)
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['fliers'], color=color)
    plt.setp(bp['medians'], color=color)
    plt.legend()
ax.set_xlabel('road density')
ax.set_ylabel('number of exiting vehicles')
#ax.set_ylim(0, 2000)
ax.set_xlim(0, 1)
ax.set_xticks(DENSITIES[1::2])
plt.grid()
fig.savefig('test.pdf', bbox_inches='tight', dpi=300)
ax.cla()

#fig = plt.figure(1)
#grid = ImageGrid(fig, 111, nrows_ncols=(1,3), axes_pad=0.1, aspect=True, 
#                 share_all=True, cbar_pad=None, cbar_mode="single")
#for i in range(3):
#    ax = grid[i]
#    im = ax.imshow(cPickle.load(files[i]), interpolation='nearest', origin='lower', 
#            cmap='jet', extent=(0,0.95,0,0.9), vmin=0, vmax=1)
##    grid[i].set_aspect('equal')
#    grid[i].set_xlabel(r'Road Density ($\rho_r$)', fontsize=16)
#cbar = grid.cbar_axes[0].colorbar(im)
#grid[0].set_title('All', fontsize=16)
#grid[1].set_title('Cars', fontsize=16)
#grid[2].set_title('Motorcycles', fontsize=16)

#grid.axes_llc.set_xticks(np.arange(0.1, 1, 0.1))
#grid.axes_llc.set_yticks(np.arange(0.1, 1, 0.1))
#grid.axes_llc.set_ylabel(r'Car Ratio ($N_{cars}/N_{total}$)', fontsize=16)
#cbar.set_label_text(r'Movement Ratio ($N_{moving}/N_{total}$)', rotation=270, fontsize=16)
#plt.show()

