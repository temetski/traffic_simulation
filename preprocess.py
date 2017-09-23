import numpy as np
import pandas as pd
import re
import glob
import json
import os
import numpy as np

def throughput(data):
    return np.sum(data.groupby("id")["vel"].sum().values)#parameters["len_road"]

def velocity_ave_car(data):
    return data.groupby("id")["vel"].mean().values

def velocity_ave_road(data):
    return data.groupby("timestep")["vel"].mean().values

def preprocess(folder):
    os.chdir(folder)
    with open("parameters.json", "r") as file:
        parameters = json.load(file)

    files = glob.glob("CarRatio*")
    densities = [float(value) for filename in files for value in re.findall("Density\.(\d.\d{2})", filename)]
    data = []
    num_trials = parameters["trials"]
    cols = ['timestep', 'id', 'pos', 'lane', 'vel', 'size', 'flag_slow']
    for density in densities:
        data_trials = np.load("CarRatio.1.00.Density.%.2f.npz" % density)['arr_0']
        data_throughput = []
        data_velocity_car = []
        for data_trial in data_trials:
            trial_data = pd.DataFrame(data_trial, columns=cols)
            data_throughput.append(throughput(trial_data))
            data_velocity_car.extend(velocity_ave_car(trial_data))
        # grouping = trial_data.groupby("id")
        dict_density = {
                        "density": density,
                        "throughput": data_throughput,
                        "velocity": data_velocity_car
                        }
        data.append(dict_density)
    data = sorted(data, key=lambda k: k['density'])
    np.save('data', data)
    os.chdir("../")

if __name__=="__main__":
    folders = glob.glob("virt*")
    for folder in folders:
        print("processing folder: ", folder)
        preprocess(folder)
