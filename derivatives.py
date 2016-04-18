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
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

def _2d_dev_(f, x, h):
    return (f[x+1] - 2*f[x] + f[x-1])/h**2


def derivative(f, dx):
    deri = []
    deri.append(_2d_dev_(f,1, dx))
    for x in range(1,len(f)-1):
        deri.append(_2d_dev_(f,x,dx))
    deri.append(_2d_dev_(f, x, dx))
    return deri

def rho_crit(m):
    B = np.array(derivative(m,0.01))[:50]
    return (np.where(np.max(B**2)==B**2)[0]+1)*0.01

def plot_derivative(m):
    A = np.gradient(m, 0.01)
    B = derivative(m,0.01)


    host = host_subplot(111, axes_class=AA.Axes)
    par = host.twinx()

    host.plot(DENSITIES, m, markeredgecolor='black',  color='0.5', markersize=6, markeredgewidth=0.2,
                    linewidth=2, marker='o', label=r'$Q$')
    par.plot(DENSITIES, A, markeredgecolor='black',  color='b', markersize=6, markeredgewidth=0.2,
                    linewidth=2, marker='o', label=r'$\dot{Q}$')
    par.ticklabel_format(useOffset=False, style='sci', axis='y', scilimits=(0,0))
    par.yaxis.major.formatter._useMathText = True
    plt.legend(loc='best')
    plt.grid()
    host.set_xlabel(r'Density ($\rho$)')
    host.set_ylabel(r'Throughput ($Q$)')
    par.set_ylabel(r'$\dot{Q}$')
    plt.savefig('../derivative_first.jpg', bbox_inches='tight')
    plt.clf()

    host = host_subplot(111, axes_class=AA.Axes)
    par = host.twinx()

    host.plot(DENSITIES, m, markeredgecolor='black',  color='0.5', markersize=6, markeredgewidth=0.2,
                    linewidth=2,marker='o', label=r'$Q$')
    par.plot(DENSITIES, np.abs(B), markeredgecolor='black',  color='r', markersize=6, markeredgewidth=0.2,
                    linewidth=2, marker='o', label=r'$|\ddot{Q}|$')
    par.ticklabel_format(useOffset=False, style='sci', axis='y', scilimits=(0,0))
    par.yaxis.major.formatter._useMathText = True
    plt.legend(loc='best')
    plt.grid()
    host.set_xlabel(r'Density ($\rho$)')
    host.set_ylabel(r'Throughput ($Q$)')
    par.set_ylabel(r'$|\ddot{Q}|$')
    plt.savefig('../derivative_second.jpg', bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    __plot_ratios__ = [0, 0.25, 0.5, 0.75, 1]

    __p_lambdas__ = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    DIRNAME = os.path.split(os.getcwd())[1]
    DENSITIES = np.arange(0.01, 1,0.01)
    _density_ = np.arange(0.05, 1,0.05)
    TEST = np.zeros((len(__plot_ratios__), len(__p_lambdas__)))
    peakdenslambda = []
    ls = [(), (11,4), "-", "--"]
    markers = ['o', '*']
    for i, p_lambda in enumerate(__p_lambdas__):
        os.chdir("lanechange_%.1f_virt_0" % p_lambda)
        all_data = np.load("data.npz")
        THROUGHPUT = all_data["THROUGHPUT"]
        MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios
        for j in range(5):
            TEST[j, i] = rho_crit(MEDIANS[j])
        os.chdir("..")

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, label, i in zip(TEST, __plot_ratios__, 
                               range(len(__plot_ratios__))):
        color = "%s" % (i*0.15)
        ax.plot(__p_lambdas__[:2], ydata[:2], color=color, linewidth=2,
                marker=markers[i%2], ls='-.', markeredgewidth=0.0)
        ax.plot(__p_lambdas__[1:], ydata[1:], color=color, linewidth=2,
                label=r"$\kappa = %.2f$" % label, marker=markers[i%2], dashes=ls[i % 2], markeredgewidth=0.0)
    ax.legend(loc="best", frameon=False, framealpha=0.6)
#    ax.text(0.02, 0.97, r"$p_{\lambda} = %.2f$, $W_v = %d$" % 
#            (LANE_CHANGE_PROB, VIRTUAL_LANES),  ha="left", va="top",
#            size=20, bbox=bbox_props, transform=ax.transAxes)
    ax.set_xlabel(r'Lanechange probability ($p_\lambda$)')
    ax.set_ylabel(r'Critical density ($\rho_{crit}$)')
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
#    ax.grid()
    fig.savefig("images/fig_lambda_crit.pdf", bbox_inches='tight', dpi=300)
    fig.clf()
    plot_derivative(MEDIANS[0])

    for i, p_lambda in enumerate(__p_lambdas__):
        if p_lambda==0:
            os.chdir("lanechange_%.1f_virt_0" % p_lambda)
        else:
            os.chdir("lanechange_%.1f_virt_1" % p_lambda)
        all_data = np.load("data.npz")
        THROUGHPUT = all_data["THROUGHPUT"]
        MEDIANS = np.median(THROUGHPUT, axis=2) # Median for trials in car ratios
        for j in range(5):
            TEST[j, i] = rho_crit(MEDIANS[j])
        os.chdir("..")
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    for ydata, label, i in zip(TEST, __plot_ratios__, 
                               range(len(__plot_ratios__))):
        color = "%s" % (i*0.15)
        ax.plot(__p_lambdas__[:2], ydata[:2], color=color, linewidth=2,
                marker=markers[i%2], ls='-.', markeredgewidth=0.0)
        ax.plot(__p_lambdas__[1:], ydata[1:], color=color, linewidth=2,
                label=r"$\kappa = %.2f$" % label, marker=markers[i%2], dashes=ls[i % 2], markeredgewidth=0.0)
    ax.legend(loc="best", frameon=False, framealpha=0.6)
    ax.set_xlabel(r'Lanechange probability ($p_\lambda$)')
    ax.set_ylabel(r'Critical density ($\rho_{crit}$)')
    ax.set_xlim(0, 1)
    ax.set_xticks(_density_[1::2])
    fig.savefig("images/fig_lambda_crit_virt.pdf", bbox_inches='tight', dpi=300)
    fig.clf()
    plot_derivative(MEDIANS[1])

