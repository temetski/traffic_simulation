#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
from __future__ import division
import numpy as np
import matplotlib
#from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
#                        VIRTUAL_LANES, SLOWDOWN, LANE_CHANGE_PROB
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
    ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=4.5,
                linewidth=2, elinewidth=1, label=r"$p_\lambda = %.2f$" % label, 
                marker=marks[i%2],dashes=ls[i%2],markeredgewidth=0.0)
#    ax.plot(DENSITIES, median, color=color, linewidth=2.5,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])

    plt.legend()



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
    RATIOS = [0, 0.25, 0.5, 0.75, 1]
    LAMBDA = [0,0.3,0.6,1]
    FILES = glob.glob("CarRatio*")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0.05, 1,0.05)
    ls = [(), (13,3)]
    marks = ['o', 's']   

    for num in [0,4]:
        to_plot = []
        for lamb in LAMBDA:
            os.chdir("lanechange_%.1f_virt_0" % lamb)
            all_data = np.load("data.npz")
            THROUGHPUT = all_data["THROUGHPUT"]
            to_plot.append(THROUGHPUT[num])
            os.chdir("..")
        MEDIANS = np.median(to_plot, axis=2) # Median for trials in car ratios
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        for ydata, label, i in zip(to_plot, LAMBDA, range(len(LAMBDA))):
            plot()
        ax.text(0.02, 0.97, r"$\kappa = %.2f$" %
                (RATIOS[num]),  ha="left", va="top",
                size=20, bbox=bbox_props, transform=ax.transAxes)
        ax.set_xlabel(r'Road density ($\rho$)')
        ax.set_ylabel('Throughput ($Q$)')
#        ax.set_ylim(0, 2500)
        ax.set_xlim(0, 1)
        ax.set_xticks(_density_[1::2])
        plt.grid()
        fig.savefig('images/p_lanechange_%.2f.pdf' % RATIOS[num], bbox_inches='tight', dpi=300)
        ax.cla()

        lceffect = []
        LAMBDA_lc = [0.1, 0.4, 0.7, 1]
        for lamb in LAMBDA_lc:
            os.chdir("lanechange_%.1f_virt_0" % lamb)
            all_data = np.load("data.npz")
            THROUGHPUT = all_data["THROUGHPUT"]
            lceffect.append(THROUGHPUT[num])
            os.chdir("..")
#        fig = plt.figure(1)
#        ax = fig.add_subplot(111)
        p0 = np.median(to_plot[0],axis=1)
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        for ydata, label, i in zip(lceffect, LAMBDA_lc, range(len(LAMBDA_lc))):
            color = "%s" % (i*0.15)
            median = np.median(ydata, axis=1)
    #            ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=4.5,
    #                        linewidth=2, elinewidth=1, label=r"$p_\lambda = %.2f$" % label, 
    #                        marker=marks[i%2],dashes=ls[i%2],markeredgewidth=0.0)
            ax.plot(DENSITIES, (median-p0), color=color, linewidth=2.5,
                        label=r"$p_\lambda = %.2f$" % label, dashes=ls[i%2])

        plt.legend(loc="best")
        ax.text(0.02, 0.97, r"$\kappa = %.2f$" %
                (RATIOS[num]),  ha="left", va="top",
                size=20, bbox=bbox_props, transform=ax.transAxes)
        ax.set_xlabel(r'Vehicle density ($\rho$)')
        ax.set_ylabel('Thoughput difference ($Q_\lambda - Q_0$)')
        ax.set_xlim(0, 1)
        ax.set_xticks(_density_[1::2])
        plt.grid()
        fig.savefig('images/lanechangeeffect_%.2f.pdf' % RATIOS[num], bbox_inches='tight', dpi=300)
        ax.cla()

    for num in range(5):
        lceffect = []
        LAMBDA_lc = np.arange(0.1,1.1,0.1)
        for lamb in LAMBDA_lc:
            os.chdir("lanechange_%.1f_virt_0" % lamb)
            all_data = np.load("data.npz")
            THROUGHPUT = all_data["THROUGHPUT"]
            lceffect.append(THROUGHPUT[num])
            os.chdir("..")
#        fig = plt.figure(1)
#        ax = fig.add_subplot(111)
        p0 = np.median(to_plot[0],axis=1)
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        plambda=[]
        for ydata in lceffect:
            median = np.median(ydata, axis=1)
            plambda.append(np.sum(median-p0))
    #            ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=4.5,
    #                        linewidth=2, elinewidth=1, label=r"$p_\lambda = %.2f$" % label, 
    #                        marker=marks[i%2],dashes=ls[i%2],markeredgewidth=0.0)
        color = "%s" % (num*0.23)
        ax.plot(LAMBDA_lc, plambda, color=color, linewidth=2, marker=marks[num%2], markersize=4.5,
                    label=r"$\kappa = %.2f$" % RATIOS[num], dashes=ls[num%2])
    plt.legend(loc="best")
    ax.set_xlabel(r'Lane hange probability ($p_\lambda$)')
    ax.set_ylabel('Total throughput difference ($Q_\lambda - Q_0$)')
    ax.set_xlim(0.1, 1)
    ax.set_xticks(_density_[1::2])
    plt.grid()
    fig.savefig('images/area_lanechangeeffect.pdf', bbox_inches='tight', dpi=300)
    ax.cla()


    for num in [0,4]:
        eff_to_plot = []
        for lamb in LAMBDA:
            os.chdir("lanechange_%.1f_virt_0" % lamb)
            all_data = np.load("data.npz")
            THROUGHPUT = all_data["EFFICIENCY"]
            eff_to_plot.append(THROUGHPUT[num])
            os.chdir("..")
        fig = plt.figure(2)
        ax = fig.add_subplot(111)
        for ydata, label, i in zip(eff_to_plot, LAMBDA, range(len(LAMBDA))):
            color = "%s" % (i*0.15)
            median = np.median(ydata, axis=1)
            errminus = median - np.percentile(ydata,25, axis=1)
            errplus = np.percentile(ydata,75, axis=1) - median
            ax.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=6,
                    linewidth=2, elinewidth=1, label=r"$p_\lambda = %.2f$" % label, 
                    marker=marks[i%2],dashes=ls[i%2], markeredgewidth=0.2, markeredgecolor='black')
            plt.legend(loc=3)
        ax.set_yscale('log')
        ax.text(0.98, 0.97, r"$\kappa = %.2f$" %
                (RATIOS[num]),  ha="right", va="top",
                size=20, bbox=bbox_props, transform=ax.transAxes)
        ax.set_xlabel(r'Vehicle density ($\rho$)')
        ax.set_ylabel('Efficiency ($\mathcal{E}$)')
        ax.set_ylim(10**-1, 1)
        ax.set_xlim(0.05, 0.5)
#        ax.set_xticks(_density_[1::2])
        plt.grid()
        fig.savefig('images/efficiency_lanechange_zoom_%s.pdf' % RATIOS[num], bbox_inches='tight', dpi=300)
        ax.cla()

        fig2 = plt.figure(1)
        ax2 = fig2.add_subplot(111)
        for ydata, label, i in zip(eff_to_plot, LAMBDA, range(len(LAMBDA))):
            color = "%s" % (i*0.15)
            median = np.median(ydata, axis=1)
            errminus = median - np.percentile(ydata,25, axis=1)
            errplus = np.percentile(ydata,75, axis=1) - median
            ax2.errorbar(DENSITIES, median, [errminus, errplus], color=color, markersize=6,
                    linewidth=2, elinewidth=1, label=r"$p_\lambda = %.2f$" % label, 
                    marker=marks[i%2],dashes=ls[i%2], markeredgewidth=0.2, markeredgecolor='black')
            plt.legend(loc=3)
        ax2.set_yscale('log')
        ax2.text(0.98, 0.97, r"$\kappa = %.2f$" %
                (RATIOS[num]),  ha="right", va="top",
                size=20, bbox=bbox_props, transform=ax2.transAxes)
        ax2.set_xlabel(r'Vehicle density ($\rho$)')
        ax2.set_ylabel(r'$\tilde{v}/v_{max}$')
        ax2.set_ylim(10**-3, 1)
        ax2.set_xlim(0, 1)
        ax2.set_xticks(_density_[1::2])
        plt.grid()
        fig2.savefig('images/efficiency_lanechange_%s.pdf' % RATIOS[num], bbox_inches='tight', dpi=300)
        ax2.cla()
