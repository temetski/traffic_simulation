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
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams.update({'axes.labelsize': 17,'legend.fontsize': 15})
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


def plot():
    color = "%s" % (i*0.15)
    median = np.median(ydata, axis=1)
    errminus = median - np.percentile(ydata,25, axis=1)
    errplus = np.percentile(ydata,75, axis=1) - median
#    ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=4.5,
#                linewidth=2, elinewidth=1, label=r"$\kappa = %.2f$" % label, 
#                marker=marks[i%2],dashes=ls[i%2])
    S = np.tile(DENSITIES,50).reshape(50,99).T
    ax.scatter(S, ydata, color=color,
                    label=r"$\kappa = %.2f$" % label, s=5)
    plt.legend()


if __name__ == "__main__":
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
    FILES = glob.glob("CarRatio*")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    RATIOS = np.array([])
    for i in FILES:
        car_ratio = float(re.findall(r"CarRatio.(\d.\d+)", i)[0])
        if car_ratio not in RATIOS and car_ratio in __plot_ratios__:
            RATIOS = np.append(RATIOS, car_ratio)
    RATIOS.sort()
    all_data = np.load("data.npz")
    THROUGHPUT = all_data["THROUGHPUT"]
    THROUGHPUT_NORM = all_data["THROUGHPUT_NORM"]
    ls = [(), (13,3)]
    marks = ['o', 's']
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

# Median for trials in car ratios
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for ydata, label, i in zip(THROUGHPUT_NORM, RATIOS, range(len(RATIOS))):
        if i in [0,4]:
            plot()
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
#            (LANE_CHANGE_PROB),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Vehicle density ($\rho$)')
    ax.set_ylabel('Weighted throughput ($Q_{weighted}$)')
    ax.set_ylim(0, 3500)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/comp_norm%s.pdf' % DIRNAME, bbox_inches='tight')
    ax.cla()

# Median for trials in car ratios
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for ydata, label, i in zip(THROUGHPUT, RATIOS, range(len(RATIOS))):
        if i in [0,4]:
            plot()
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
#            (LANE_CHANGE_PROB),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Vehicle density ($\rho$)')
    ax.set_ylabel('Throughput ($Q$)')
    ax.set_ylim(0, 2800)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/comp_%s.pdf' % DIRNAME, bbox_inches='tight')
    ax.cla()

    through = np.mean(THROUGHPUT, axis=2)
    s = through[0]/through[4]
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.scatter(DENSITIES, s, s=6, color="0.3")
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
#            (LANE_CHANGE_PROB),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Road density ($\rho$)')
    ax.set_ylabel('Occupancy ($\Omega$)')
    ax.set_ylim(0, 5)
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('../images/occupancy_%s.pdf' % DIRNAME, bbox_inches='tight')
    ax.cla()

