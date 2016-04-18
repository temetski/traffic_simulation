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
    plambda = np.arange(0,1.1,0.1)
    RATIOS = np.arange(0,1.1,0.25)

    kappa = -1
    alpha = 1
    beta = 1
    gamma = 1

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    marks = ['o', 's']
    for i, p in enumerate(plambda[::2]):
        all_data = np.load("lanechange_%.1f_virt_0/collision.npz" % p)
        COLLISION = all_data["COLLISION"]
        # randdata = COLLISION[kappa,:,:,0]
        v_less = np.mean(COLLISION[kappa,:,:], axis=1)
        collision_index = (1-alpha)*DENSITIES**gamma+beta*v_less
        errminus = v_less - np.percentile(COLLISION[kappa,:,:],25, axis=1)
        errplus = np.percentile(COLLISION[kappa,:,:],75, axis=1) - v_less
        ax.errorbar(DENSITIES, collision_index, [errminus, errplus], color='%s'%(i*0.15),marker=marks[i%2], markersize=6, markeredgecolor='black',
                linewidth=2, elinewidth=1, label=r"$p_\lambda=%.2f$"%p, markeredgewidth=0.2)
    ax.legend(fontsize=18, scatterpoints=1, loc="lower center")
    ax.set_ylabel(r'Collision Index')
    ax.set_xlabel(r'Vehicle Density ($\rho$)')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1)
    plt.grid()
    fig.savefig('images/v_less.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

    for i, p in enumerate(plambda[2::2]):
        all_data = np.load("lanechange_%.1f_virt_1/collision.npz" % p)
        COLLISION = all_data["COLLISION"]
        # randdata = COLLISION[kappa,:,:,0]
        v_less = np.mean(COLLISION[kappa,:,:], axis=1)
        collision_index = (1-alpha)*DENSITIES**gamma+beta*v_less
        errminus = v_less - np.percentile(COLLISION[kappa,:,:],25, axis=1)
        errplus = np.percentile(COLLISION[kappa,:,:],75, axis=1) - v_less
        ax.errorbar(DENSITIES, collision_index, [errminus, errplus], color='%s'%(i*0.15),marker=marks[i%2], markersize=6, markeredgecolor='black',
                linewidth=2, elinewidth=1, label=r"$p_\lambda=%.2f$"%p, markeredgewidth=0.2)
    ax.legend(fontsize=18, scatterpoints=1, loc="lower center")
    ax.set_ylabel(r'Collision Index')
    ax.set_xlabel(r'Vehicle Density ($\rho$)')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1)
    plt.grid()
    fig.savefig('images/v_less_virt.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

    for i, alpha in enumerate(np.arange(0,1.1,0.25)):
        all_data = np.load("lanechange_1.0_virt_0/collision.npz")
        COLLISION = all_data["COLLISION"]
        # randdata = COLLISION[kappa,:,:,0]
        v_less = np.mean(COLLISION[kappa,:,:], axis=1)
        collision_index = (1-alpha)*DENSITIES**gamma+beta*v_less
        errminus = v_less - np.percentile(COLLISION[kappa,:,:],25, axis=1)
        errplus = np.percentile(COLLISION[kappa,:,:],75, axis=1) - v_less
        ax.errorbar(DENSITIES, collision_index, [errminus, errplus], color='%s'%(i*0.15),marker=marks[i%2], markersize=6, markeredgecolor='black',
                linewidth=2, elinewidth=1, label=r"$\alpha=%.2f$"%alpha, markeredgewidth=0.2)
    ax.legend(fontsize=18, scatterpoints=1, loc="upper left")
    ax.set_ylabel(r'Collision Index')
    ax.set_xlabel(r'Vehicle Density ($\rho$)')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1)
    plt.grid()
    fig.savefig('images/safety_alpha.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

    for i, alpha in enumerate(np.arange(0,1.1,0.25)):
        all_data = np.load("lanechange_1.0_virt_1/collision.npz")
        COLLISION = all_data["COLLISION"]
        # randdata = COLLISION[kappa,:,:,0]
        v_less = np.mean(COLLISION[kappa,:,:], axis=1)
        collision_index = (1-alpha)*DENSITIES**gamma+beta*v_less
        errminus = v_less - np.percentile(COLLISION[kappa,:,:],25, axis=1)
        errplus = np.percentile(COLLISION[kappa,:,:],75, axis=1) - v_less
        ax.errorbar(DENSITIES, collision_index, [errminus, errplus], color='%s'%(i*0.15),marker=marks[i%2], markersize=6, markeredgecolor='black',
                linewidth=2, elinewidth=1, label=r"$\alpha=%.2f$"%alpha, markeredgewidth=0.2)
    ax.legend(fontsize=18, scatterpoints=1, loc="upper left")
    ax.set_ylabel(r'Collision Index')
    ax.set_xlabel(r'Vehicle Density ($\rho$)')
    plt.locator_params(axis = 'x', nbins = 5)
    ax.set_xlim(0, 1)
    plt.grid()
    fig.savefig('images/safety_alpha_virt.pdf', bbox_inches='tight', dpi=300)
    ax.cla()

#     fig = plt.figure(1)
#     ax = fig.add_subplot(111)
#     for i, ndens in enumerate([9,19, 49]):
#         randdata = []
#         v_less = []
#         for p in np.arange(0.1,1.1,0.1):
#             all_data = np.load("lanechange_%.1f_virt_0/collision.npz" % p)
#             COLLISION = all_data["COLLISION"]
#             randdata.append(COLLISION[kappa,ndens,:,0])
#             v_less.append(COLLISION[kappa,ndens,:,1])
#         randdata = np.array(randdata).flatten()
#         v_less = np.array(v_less).flatten()
#         slope, inter, r, pval, std = linregress(randdata, v_less)
#         x = np.arange(1000)
#         ax.plot(x, x*slope+inter, color='r', zorder=0)
#         ax.scatter(randdata, v_less, color='%s'%(i*0.4), edgecolor='black', linewidth=0.1, s=13,
#                     label=r"$\rho=%.2f$"%DENSITIES[ndens])
#         xcoord = 500
#         ycoord = lambda x: x*slope+inter
#     ax.annotate(r"$r = %.2f$" % r, xy=(xcoord, ycoord(xcoord)), xycoords='data',
#     xytext=(xcoord-50,ycoord(xcoord)+1200), textcoords='data')
#     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#     ax.yaxis.major.formatter._useMathText = True
#     ax.set_ylabel(r'Number of vehicle decelerations')
#     ax.set_xlabel('Number of random slowdown events')
#     plt.locator_params(axis = 'x', nbins = 5)
#     ax.set_xlim(0, 1000)
#     plt.grid()
#     fig.savefig('images/rdata_ppt.pdf', bbox_inches='tight', dpi=300)
#     ax.cla()
#
#     fig = plt.figure(1)
#     ax = fig.add_subplot(111)
#     for dat in ['rand', 'rand_all']:
#         if dat=='rand_all':
#             color = ['r','g','b']
#         else:
#             color = ['%s'%(i*0.4) for i in range(3)]
#         for i, ndens in enumerate([9,19, 49]):
#             randdata = []
#             v_less = []
#             for p in np.arange(0.1,1.1,0.1):
#                 all_data = np.load("lanechange_%.1f_virt_0/%s.npz" % (p,dat))
#                 COLLISION = all_data["COLLISION"]
#                 randdata.append(COLLISION[kappa,ndens,:,0])
#                 v_less.append(COLLISION[kappa,ndens,:,1])
#             randdata = np.array(randdata).flatten()
#             v_less = np.array(v_less).flatten()
#             slope, inter, r, pval, std = linregress(randdata, v_less)
#             print(slope, r)
# #            x = np.arange(1000)
# #            ax.plot(x, x*slope+inter, color='r', zorder=0)
#             ax.scatter(randdata, v_less, color=color[i], edgecolor='black', linewidth=0.1, s=13,
#                         label=r"$\rho=%.2f$"%DENSITIES[ndens])
# #            xcoord = 500
# #            ycoord = lambda x: x*slope+inter
# #    ax.annotate(r"$r = %.2f$" % r, xy=(xcoord, ycoord(xcoord)), xycoords='data',
# #                xytext=(xcoord-50,ycoord(xcoord)+1200), textcoords='data')
#     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#     ax.yaxis.major.formatter._useMathText = True
#     ax.set_ylabel(r'Number of vehicle decelerations')
#     ax.set_xlabel('Number of random slowdown events')
#     plt.locator_params(axis = 'x', nbins = 5)
# #    ax.set_xlim(0, 1000)
#     plt.grid()
#     fig.savefig('images/rdata_ppt_all.pdf', bbox_inches='tight', dpi=300)
#     ax.cla()
