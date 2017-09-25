from __future__ import division
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({'axes.labelsize': 18})
import matplotlib.pyplot as plt
import seaborn as sns
rc = {'font.size':16,
      'legend.fontsize':16,
      'axes.labelsize':18,
      'xtick.labelsize':16,
      'ytick.labelsize':16}
sns.set_context('paper', rc=rc)
sns.set_style("white")
sns.set_palette('colorblind')
# sns.set(font_scale=2)
# sns.axes_style
