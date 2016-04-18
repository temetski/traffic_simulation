#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
from __future__ import division
import numpy as np
import matplotlib
from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
                        VIRTUAL_LANES, SLOWDOWN, LANE_CHANGE_PROB
matplotlib.use("Agg")
matplotlib.rcParams.update({'font.size': 17})
matplotlib.rcParams.update({'axes.labelsize': 21,'legend.fontsize': 17})
import matplotlib.pyplot as plt
#plt.rc('font',family='serif')
plt.rc('font',serif='Helvetica')
import glob
import re
import os
from subprocess import call
import h5py


#REAL_LANES = 4
#ROADLENGTH = 100
#TRIALS = 50

#AREA = 1 * (REAL_LANES) * ROADLENGTH
POS = 0
LANE = 1
SPEED = 2
SIZE = 3
LAST = -1
labels = ["Motorcycle","Cars","Jeeps","Buses"]

def plot():
    color = "%s" % (i*0.15)
    median = np.median(ydata, axis=1)
    errminus = median - np.percentile(ydata,25, axis=1)
    errplus = np.percentile(ydata,75, axis=1) - median
    ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=4.5,
                linewidth=2, elinewidth=1, label=r"$\kappa$=%.1f"%label, 
                marker=marks[i%2],dashes=ls[i%2], markeredgewidth=0.0)
#    ax.plot(DENSITIES, median, color=color, linewidth=2.5,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])

    plt.legend()


if __name__ == "__main__":
    __plot_ratios__ = [0,0.25,0.5,0.75,1]
    FILES = glob.glob("CarRatio*")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    RATIOS = __plot_ratios__
    all_data = np.load("data.npz")
    THROUGHPUT = all_data["THROUGHPUT"]
    THROUGHPUT_CAR = all_data["THROUGHPUT_CAR"]
    THROUGHPUT_NORM = all_data["THROUGHPUT_NORM"]
    VELOCITIES = all_data["VELOCITIES"]
    LCCOUNT = all_data["LCCOUNT"]
    EFFICIENCY = all_data["EFFICIENCY"]
    ls = [(), (13,3)]
    marks = ['o', 's']

    MEDIANS = np.median(THROUGHPUT_NORM, axis=2) # Median for trials in car ratios
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, label, i in zip(THROUGHPUT_NORM, RATIOS, range(len(RATIOS))):
        if i in  [0,4]:
            plot()
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
#            (LANE_CHANGE_PROB),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Volume throughput ($Q_{v}$)')
#    ax.set_ylim(0, 1000)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/comp_norm%s.pdf' % DIRNAME, bbox_inches='tight', dpi=300)
    ax.cla()

    MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, label, i in zip(THROUGHPUT, RATIOS, range(len(RATIOS))):
        if i in  [0,4]:
            plot()
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
#            (LANE_CHANGE_PROB),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Throughput ($Q$)')
#    ax.set_ylim(0, 1000)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/comp_%s.pdf' % DIRNAME, bbox_inches='tight', dpi=300)
    ax.cla()


