#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 00:18:38 2013

@author: Damian
"""
import numpy as np
import matplotlib
#from load_params import ROADLENGTH, TRIALS, REAL_LANES, \
#                        VIRTUAL_LANES, SLOWDOWN, LANE_CHANGE_PROB
matplotlib.use("Agg")
matplotlib.rcParams.update({'font.size': 15})
matplotlib.rcParams.update({'axes.labelsize': 17,'legend.fontsize': 15})
import matplotlib.pyplot as plt
from pylab import cm
import glob
import re
import os
from subprocess import call
import h5py

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
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
#    __plot_ratios__ = np.arange(0, 1.1, 0.1)
    __p_lambdas__ = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1,0.01)
    _density_ = np.arange(0.05, 1,0.05)
    TEST = []
    peakdenslambda = []
    varlambda = []
    ls = [(), (11,4), "-", "--"]
    markers = ['o', '*']
    for p_lambda in __p_lambdas__:
        os.chdir("lanechange_%.1f_virt_0" % p_lambda)
        all_data = np.load("data.npz")
        THROUGHPUT = all_data["THROUGHPUT"]
        MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios
        PEAKS = np.max(MEDIANS, axis=1)
        PEAKDENS = np.argmax(MEDIANS, axis=1)
        variance = np.std(THROUGHPUT, axis=2)[range(5),PEAKDENS]
        os.chdir("..")
        TEST.append(PEAKS)
        peakdenslambda.append(DENSITIES[PEAKDENS])
        varlambda.append(variance)
    vlam = varlambda
    varlambda = np.array(varlambda).transpose()
    peaks_lambda = np.array(TEST).transpose()
    peakdenslambda = np.array(peakdenslambda).transpose()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, error, label, i in zip(peaks_lambda, varlambda, __plot_ratios__,
                               range(len(__plot_ratios__))):
        color = "%s" % (i*0.15)
        ax.errorbar(__p_lambdas__[:2], ydata[:2], yerr=error[:2], color=color, linewidth=1.5,
                marker=markers[i%2], ls='-.', markeredgewidth=0.0)
        ax.errorbar(__p_lambdas__[1:], ydata[1:], yerr=error[1:], color=color, linewidth=1.5,
                label=r"$\kappa = %.2f$" % label, marker=markers[i%2], dashes=ls[i % 2], markeredgewidth=0.0)
        ax.fill_between(__p_lambdas__,ydata+error, ydata-error, color="%s" % (i*0.15+0.2))
    ax.legend(loc="best", frameon=False, framealpha=0.6)
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" %
#            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Lanechange probability ($p_\lambda$)')
    ax.set_ylabel('Peak throughput ($Q_{peak}$)')
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
#    ax.grid()
    fig.savefig("images/fig_lambda.pdf", bbox_inches='tight', dpi=300)
    fig.clf()

#    cmap = cm.get_cmap('gray', int((np.max(peakdenslambda)-np.min(peakdenslambda))/0.05+1.1))
#    im = ax2.matshow(peakdenslambda, cmap=cmap,
#                     interpolation='nearest', aspect=True)#extent=(0.1,1,0,1))
#    ax2.set_xticks(range(11))
#    ax2.set_xticklabels(list(np.arange(0, 1.1, 0.1)))
#    ax2.set_yticks(range(5))
#    ax2.set_yticklabels(__plot_ratios__)
#    cbar = fig2.colorbar(im, ticks=np.arange(np.min(peakdenslambda),np.max(peakdenslambda)+0.01,0.05))
#    cbar.set_label(r'Peak density ($\rho$)')

#    for ydata, label, i in zip(peakdenslambda, __plot_ratios__,
#                               range(len(__plot_ratios__))):
#        color = "%s" % (i*0.15)
#        ax2.plot(__p_lambdas__[:2], ydata[:2], color=color, linewidth=2,
#                marker=markers[i%2], ls='-.', markeredgewidth=0.0)
#        ax2.plot(__p_lambdas__[1:], ydata[1:], color=color, linewidth=2,
#                label=r"$\kappa = %.2f$" % label, marker=markers[i%2], dashes=ls[i % 2], markeredgewidth=0.0)
#    ax2.legend(loc="center right", frameon=False)
##        ax2.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
##    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" %
##            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
##            size=20, bbox=bbox_props, transform=ax.transAxes)
#    ax2.set_xlim(0, 1)
#    ax2.set_xticks(_density_[1::2])
##    ax2.grid()
#    ax2.set_xlabel(r'Lanechange probability ($p_\lambda$)')
#    ax2.set_ylabel(r'Density of peak throughput ($\rho$)')
#    fig2.savefig("images/ratio_lambda.pdf", bbox_inches='tight', dpi=300)
#    fig2.clf()

    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    for i, s in enumerate([(9,0),(17,4)]):
        ndens = s[0]
        kappa = s[1]
        vardata = []
        for p in np.arange(0,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/data.npz" % p)
            RANDSTOP = all_data["THROUGHPUT"]
            vardata.append(RANDSTOP[kappa,ndens,:])
        vardata = np.array(vardata)
        means = np.mean(vardata, axis=1)
        var = np.std(vardata, axis=1)
        ax2.plot(np.arange(0,1.1,0.1), var, color='%s'%(i*0.8), marker='o', markeredgecolor='black', linewidth=1.5, markersize=10,
                    label=r"$\rho=%.2f, \kappa=%0.1f$"%(DENSITIES[ndens], __plot_ratios__[kappa]))
    ax2.legend(fontsize=17, numpoints=1)
    ax2.set_ylabel(r'Variance of throughput ($\sigma^2(Q)$)')
    ax2.set_xlabel(r'Lanechange probability ($p_\lambda$)')
#    plt.locator_params(axis = 'x', nbins = 5)
#        ax.set_ylim(0, 3300)
#    ax.set_xlim(0, 1000)
    ax2.grid()
    fig2.savefig('images/variance.pdf', bbox_inches='tight', dpi=300)
    ax2.cla()

    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    for i, s in enumerate([(9,0),(17,4)]):
        ndens = s[0]
        kappa = s[1]
        vardata = []
        for p in np.arange(0,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/data.npz" % p)
            RANDSTOP = all_data["THROUGHPUT"]
            vardata.append(RANDSTOP[kappa,ndens,:])
        vardata = np.array(vardata)
        means = np.mean(vardata, axis=1)
        var = np.std(vardata, axis=1)
        ax2.plot(np.arange(0,1.1,0.1), var, color='%s'%(i*0.8), marker='o', markeredgecolor='black', linewidth=1.5, markersize=10,
                    label=r"$\rho=%.2f$"%(DENSITIES[ndens]))
    ax2.legend(fontsize=17, numpoints=1)
    ax2.set_ylabel(r'Variance of throughput ($\sigma^2(Q)$)')
    ax2.set_xlabel(r'Lanechange probability ($p_\lambda$)')
#    plt.locator_params(axis = 'x', nbins = 5)
#        ax.set_ylim(0, 3300)
#    ax.set_xlim(0, 1000)
    ax2.grid()
    fig2.savefig('images/variance_ppt.pdf', bbox_inches='tight', dpi=300)
    ax2.cla()

#    __p_lambdas__ = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
#    DIRNAME = os.path.split(os.getcwd())[1]
#    TEST = []
#    peakdenslambda = []
#    for p_lambda in __p_lambdas__:
#        os.chdir("lanechange_%.1f_virt_1" % p_lambda)
#        all_data = np.load("data.npz")
#        THROUGHPUT = all_data["THROUGHPUT"]
#        MEDIANS = np.median(THROUGHPUT, axis=2)  # Median for trials in car ratios
#        PEAKS = np.max(MEDIANS, axis=1)
#        PEAKDENS = np.argmax(MEDIANS, axis=1)
#        os.chdir("..")
#        TEST.append(PEAKS)
#        peakdenslambda.append(DENSITIES[PEAKDENS])
#    peaks_lambda = np.array(TEST).transpose()
#    peakdenslambda = np.array(peakdenslambda).transpose()
#    fig = plt.figure(1)
#    ax = fig.add_subplot(111)
#    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
#    for ydata, label, i in zip(peaks_lambda, __plot_ratios__,
#                               range(len(__plot_ratios__))):
#        color = "%s" % (i*0.15)
#        ax.plot(__p_lambdas__, ydata, color=color, linewidth=3,
#                label=r"$\kappa = %.2f$" % label, dashes=ls[i % 2])
#        ax.scatter(__p_lambdas__, ydata, color=color)
##        plt.legend()
##    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" %
##            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
##            size=20, bbox=bbox_props, transform=ax.transAxes)
#    ax.set_xlabel(r'Lanechange probability ($p_\lambda$)')
#    ax.set_ylabel('Peak throughput')
#    ax.set_xlim(0, 1)
#    ax.set_xticks(DENSITIES[1::2])
#    ax.grid()
#    fig.savefig("images/fig_lambda_virt.pdf", bbox_inches='tight', dpi=300)
#    fig.clf()
#
#    fig2 = plt.figure(2)
#    ax2 = fig2.add_subplot(111)
#    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

##    cmap = cm.get_cmap('gray', int((np.max(peakdenslambda)-np.min(peakdenslambda))/0.05+1.1))
##    im = ax2.matshow(peakdenslambda, cmap=cmap,
##                     interpolation='nearest', aspect=True)#extent=(0.1,1,0,1))
##    ax2.set_xticks(np.arange(10))
##    ax2.set_xticklabels(list(np.arange(0.1, 1.1, 0.1)))
##    ax2.set_yticks(range(5))
##    ax2.set_yticklabels(__plot_ratios__)
##    cbar = fig2.colorbar(im, ticks=np.arange(np.min(peakdenslambda),np.max(peakdenslambda)+0.01,0.05))
##    cbar.set_label(r'Peak density ($\rho$)')

#    ax2.grid()
#    for ydata, label, i in zip(peakdenslambda, __plot_ratios__,
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
#    ax2.grid()

#    ax2.set_xlabel(r'Lanechange probability ($p_\lambda$)')
#    ax2.set_ylabel(r'Car fraction ($\kappa$)')
#    fig2.savefig("images/ratio_lambda_virt.pdf", bbox_inches='tight', dpi=300)
#    fig2.clf()
