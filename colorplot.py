#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import matplotlib
from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
                        VIRTUAL_LANES, SLOWDOWN, LANE_CHANGE_PROB
matplotlib.use("Agg")
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams.update({'axes.labelsize': 17})
import matplotlib.pyplot as plt
from pylab import cm
import glob
import re
import os
from subprocess import call
import h5py
from matplotlib.colors import LinearSegmentedColormap

#AREA = 1 * (REAL_LANES) * ROADLENGTH
SPEED = -2
SIZE = -1
LAST = -1
LANE = 1

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
#    cdict = {'red':   ((0.0, 0,0), 
#                       (0.7, 0,0),  # red 
#                       (0.96, .97,.97),  # violet
#                       (1.0, 1.0,1)), # blue

#             'green': ((0.0, 0,0), 
#                       (0.7, 0,0),  # red 
#                       (0.9, 1.0,1),  # violet
#                       (1.0, 1.0,1)), # blue

#             'blue':  ((0.0, 0.0,0),  # red
#                       (0.3, 1.0,1),  # violet
#                       (1.0, 1.0,1))  # blue
#              }
    cdict = {'red':   ((0.0, 0,0), 
                       (0.3, 0.3,0.3),  # red 
                       (0.96, .98,.98),  # violet
                       (1.0, 1.0,1)), # blue
            'green':   ((0.0, 0,0), 
                       (0.3, 0.3,0.3),  # red 
                       (0.96, .98,.98),  # violet
                       (1.0, 1.0,1)), # blue
            'blue':   ((0.0, 0,0), 
                       (0.3, 0.3,0.3),  # red 
                       (0.96, .98,.98),  # violet
                       (1.0, 1.0,1)) # blue
              }
    hot2 = LinearSegmentedColormap('Hot2', cdict)
    plt.register_cmap(cmap=hot2)
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
#    __plot_ratios__ = np.arange(0, 1.1, 0.1)
    __p_lambdas__ = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1,0.01)
    _density_ = np.arange(0.05, 1,0.05)
    TEST = []
    ls = [(), (15,2), "-", "--"]
    for p_lambda in __p_lambdas__:
        os.chdir("lanechange_%.1f_virt_0" % p_lambda)
#        for d, density in enumerate(DENSITIES):     
        all_data = np.load("data.npz")
        EFFICIENCY = all_data["EFFICIENCY"]
        MEDIANS = np.median(EFFICIENCY, axis=2) # Median for trials in car ratios
        EFFI = np.log(MEDIANS[0, :])
#        EFFI = MEDIANS[4, :]
        os.chdir("..")
        TEST.append(EFFI)
    peaks_lambda = np.array(TEST).transpose()

    
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    cmap=  plt.get_cmap('Hot2')
#    cmap = cm.get_cmap('gray', int((np.max(TEST)-np.min(TEST))/0.05+1.1))
    im = ax2.matshow(TEST, cmap=cmap, origin='lower',
                     interpolation='nearest', aspect=True, extent=(0.1,1,0,1), vmin=-3)
    ax2.set_xticks(np.arange(0.1, 1.1, 0.1))
    ax2.set_xticklabels(list(np.arange(0, 1.1, 0.1)))
    ax2.set_yticks(__p_lambdas__)
    ax2.set_yticklabels(__p_lambdas__)
    cbar = fig2.colorbar(im)
    cbar.set_label(r'Efficiency')
    
#    for ydata, label, i in zip(TEST, __plot_ratios__, 
#                               range(len(__plot_ratios__))):
#        color = "%s" % (i*0.15)
#        ax2.plot(__p_lambdas__, ydata, color=color, linewidth=3,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i % 2])
#        ax2.scatter(__p_lambdas__, ydata, color=color)
##        plt.legend()
##    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" % 
##            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
##            size=20, bbox=bbox_props, transform=ax.transAxes)
#    ax2.set_xlim(0, 1)
#    ax2.set_xticks(_density_[1::2])
#    ax2.grid()

    ax2.set_ylabel(r'Lanechange probability ($p_\lambda$)')
    ax2.set_xlabel(r'Density ($\rho$)')
    fig2.savefig("images/test.pdf", bbox_inches='tight', dpi=300)
    fig2.clf()
    
