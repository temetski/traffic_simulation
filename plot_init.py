from __future__ import division
import numpy as np
import os
import matplotlib
if os.name == 'posix' and "DISPLAY" not in os.environ:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
rc = {'font.size':16,
      'legend.fontsize':16,
      'axes.labelsize':18,
      'xtick.labelsize':16,
      'ytick.labelsize':16}
sns.set(context="paper", style="white", palette="colorblind", rc=rc)