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
matplotlib.rcParams.update({'axes.labelsize': 17})
import matplotlib.pyplot as plt
import glob
import re
import os
from subprocess import call
import h5py
from scipy.stats import linregress

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
    color = "%s" % (i*0.4)
    median = np.median(ydata, axis=1)
    errminus = median - np.percentile(ydata,25, axis=1)
    errplus = np.percentile(ydata,75, axis=1) - median
    ax.errorbar(DENSITIES, median, [errminus, errplus], color=color,
                linewidth=2.5)
    ax.plot(DENSITIES, median, color=color, linewidth=2.5,
                label=r"$\kappa = %.2f$" % label, dashes=ls[i%2])
    plt.legend()



if __name__ == "__main__":
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]
    FILES = glob.glob("CarRatio*")
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1, 0.01)
    _density_ = np.arange(0, 1.01,0.05)
    plambda = np.arange(0.1,1.1,0.1)
    RATIOS = np.arange(0,1.1,0.25)
    markertype = ['s', '^', '*']

    ndens = 50
    kappa = -1

    for i, ndens in enumerate([9,19, 49]):
        randdata = []
        decedata = []
        for p in np.arange(0.1,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/rand.npz" % p)
            RANDSTOP = all_data["RANDSTOP"]
            randdata.append(RANDSTOP[kappa,ndens,:,0])
            decedata.append(RANDSTOP[kappa,ndens,:,1])
    #    ls = [(), (15,2), "-", "--"]
        norm = (1000*DENSITIES[ndens]*ROADLENGTH*REAL_LANES)
        randdata = np.array(randdata)/norm
        decedata = np.array(decedata)/norm
#        r = decedata
        r = randdata
        median = np.median(r, axis=1) # Median for trials in car ratios
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        color = "%s" % (i*0.40)
        errminus = median - np.percentile(r,25, axis=1)
        errplus = np.percentile(r,75, axis=1) - median
        ax.errorbar(plambda, median, [errminus, errplus],color=color)
        ax.plot(plambda, median, linewidth=2., marker=markertype[i], markersize=8, color=color, label=r"$\rho = %.2f$" % DENSITIES[ndens])
###    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax.legend()
    #    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
    #            (LANE_CHANGE_PROB),  ha="left", va="top",
    #            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True
    ax.set_xlabel(r'Lane changing probability ($p_\lambda$)')
    ax.set_ylabel('Occurrence of random slowdowns')
#    ax.set_ylim(0, 3300)
    ax.set_xlim(0, 1.01)
    ax.set_xticks(_density_[::2])
    plt.grid()
    fig.savefig('images/rplot.pdf', bbox_inches='tight', dpi=300)
    ax.cla()
    for i, ndens in enumerate([19, 49]):
        randdata = []
        decedata = []
        for p in np.arange(0.1,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/rand.npz" % p)
            RANDSTOP = all_data["RANDSTOP"]
            randdata.append(RANDSTOP[kappa,ndens,:,0])
            decedata.append(RANDSTOP[kappa,ndens,:,1])
    #    ls = [(), (15,2), "-", "--"]
        norm = (1000*DENSITIES[ndens]*ROADLENGTH*REAL_LANES)
        randdata = np.array(randdata)/norm
        decedata = np.array(decedata)/norm
#        r = decedata
        r = randdata
        median = np.median(r, axis=1) # Median for trials in car ratios
        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        color = "%s" % (i*0.40)
        errminus = median - np.percentile(r,25, axis=1)
        errplus = np.percentile(r,75, axis=1) - median
        ax.errorbar(plambda, median, [errminus, errplus],color=color)
        ax.plot(plambda, median, linewidth=2., marker=markertype[i], markersize=8, color=color, label=r"$\rho = %.2f$" % DENSITIES[ndens])
###    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax.legend()
    #    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$" %
    #            (LANE_CHANGE_PROB),  ha="left", va="top",
    #            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True
    ax.set_xlabel(r'Lane changing probability ($p_\lambda$)')
    ax.set_ylabel('Occurrence of random slowdowns')
#    ax.set_ylim(0, 3300)
    ax.set_xlim(0, 1.01)
    ax.set_xticks(_density_[::2])
    plt.grid()
    fig.savefig('images/rplot_ppt.pdf', bbox_inches='tight', dpi=300)
    ax.cla()


    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for i, ndens in enumerate([9,19, 49]):
        randdata = []
        decedata = []
        for p in np.arange(0.1,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/rand.npz" % p)
            RANDSTOP = all_data["RANDSTOP"]
            randdata.append(RANDSTOP[kappa,ndens,:,0])
            decedata.append(RANDSTOP[kappa,ndens,:,1])
        randdata = np.array(randdata).flatten()
        decedata = np.array(decedata).flatten()
        slope, inter, r, pval, std = linregress(randdata, decedata)
        x = np.arange(1000)        
        ax.plot(x, x*slope+inter, color='r', zorder=0)
        ax.scatter(randdata, decedata, color='%s'%(i*0.4), marker=markertype[i], edgecolor='black', linewidth=0.1, s=18, 
                    label=r"$\rho=%.2f$"%DENSITIES[ndens])
        xcoord = 500
        ycoord = lambda x: x*slope+inter
    	ax.annotate(r"$r = %.2f$" % r, xy=(xcoord, ycoord(xcoord)), xycoords='data',
    			xytext=(xcoord-50,ycoord(xcoord)+1200), textcoords='data')
    ax.legend(loc=5, fontsize=18, scatterpoints=1)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True
    ax.set_ylabel(r'Number of vehicle decelerations')
    ax.set_xlabel('Number of random slowdown events')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1000)
    plt.grid()
    fig.savefig('images/rdata.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for i, ndens in enumerate([9,19, 49]):
        randdata = []
        decedata = []
        for p in np.arange(0.1,1.1,0.1):
            all_data = np.load("lanechange_%.1f_virt_0/rand.npz" % p)
            RANDSTOP = all_data["RANDSTOP"]
            randdata.append(RANDSTOP[kappa,ndens,:,0])
            decedata.append(RANDSTOP[kappa,ndens,:,1])
        randdata = np.array(randdata).flatten()
        decedata = np.array(decedata).flatten()
        slope, inter, r, pval, std = linregress(randdata, decedata)
        x = np.arange(1000)        
        ax.plot(x, x*slope+inter, color='r', zorder=0)
        ax.scatter(randdata, decedata, color='%s'%(i*0.4), edgecolor='black', linewidth=0.1, s=13, 
                    label=r"$\rho=%.2f$"%DENSITIES[ndens])
        xcoord = 500
        ycoord = lambda x: x*slope+inter
    ax.annotate(r"$r = %.2f$" % r, xy=(xcoord, ycoord(xcoord)), xycoords='data',
    xytext=(xcoord-50,ycoord(xcoord)+1200), textcoords='data')
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True
    ax.set_ylabel(r'Number of vehicle decelerations')
    ax.set_xlabel('Number of random slowdown events')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1000)
    plt.grid()
    fig.savefig('images/rdata_ppt.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for dat in ['rand', 'rand_all']:
        if dat=='rand_all':
            color = ['r','g','b']
        else:
            color = ['%s'%(i*0.4) for i in range(3)]
        for i, ndens in enumerate([9,19, 49]):
            randdata = []
            decedata = []
            for p in np.arange(0.1,1.1,0.1):
                all_data = np.load("lanechange_%.1f_virt_0/%s.npz" % (p,dat))
                RANDSTOP = all_data["RANDSTOP"]
                randdata.append(RANDSTOP[kappa,ndens,:,0])
                decedata.append(RANDSTOP[kappa,ndens,:,1])
            randdata = np.array(randdata).flatten()
            decedata = np.array(decedata).flatten()
            slope, inter, r, pval, std = linregress(randdata, decedata)
            print(slope, r)
#            x = np.arange(1000)        
#            ax.plot(x, x*slope+inter, color='r', zorder=0)
            ax.scatter(randdata, decedata, color=color[i], edgecolor='black', linewidth=0.1, s=13, 
                        label=r"$\rho=%.2f$"%DENSITIES[ndens])
#            xcoord = 500
#            ycoord = lambda x: x*slope+inter
#    ax.annotate(r"$r = %.2f$" % r, xy=(xcoord, ycoord(xcoord)), xycoords='data',
#                xytext=(xcoord-50,ycoord(xcoord)+1200), textcoords='data')
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.yaxis.major.formatter._useMathText = True
    ax.set_ylabel(r'Number of vehicle decelerations')
    ax.set_xlabel('Number of random slowdown events')
    plt.locator_params(axis = 'x', nbins = 5)
#    ax.set_xlim(0, 1000)
    plt.grid()
    fig.savefig('images/rdata_ppt_all.pdf', bbox_inches='tight', dpi=300)
    ax.cla()
