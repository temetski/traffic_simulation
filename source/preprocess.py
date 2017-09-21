import numpy as np
import pandas as pd

parameters = {
    "num_lanes": 4,
    "len_road": 50,
    "density": 0.1,
    "car_ratio": 1,
    "is_periodic": True,
    "timesteps": 1000,
    "p_lambda": 1,
    "num_virt_lanes": 0,
    "transient": 100,
    "layby_transient": 100
}


def throughput(data):
    return np.sum(data.groupby("id")["vel"].sum().values)//parameters["len_road"]

def velocity_ave_car(data):
    return data.groupby("id")["vel"].mean().values

def velocity_ave_road(data):
    return data.groupby("timestep")["vel"].mean().values

data = np.load("../CarRatio.1.00.Density.0.05.npz")

trials = data['arr_0']

cols = ['timestep', 'id', 'pos', 'lane', 'vel', 'size', 'flag_slow']
trial_data = pd.DataFrame(trials[0], columns=cols)

grouping = trial_data.groupby("id")

print(throughput(trial_data))
print(velocity_ave_car(trial_data))