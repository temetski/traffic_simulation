from pytraffic import PyRoad
import numpy as np
import os
import itertools
import json
from functools import partial
from multiprocessing import Pool

base_parameters = {
    "num_lanes": 4,
    "len_road": 50,
#    "density": 0.1,
    "car_ratio": 1,
    "is_periodic": True,
    "timesteps": 1000,
    "p_lambda": 1,
    "num_virt_lanes": 1,
    "transient": 100,
    "layby_transient": 100,
    "trials": 1
}

def run_trials(density, **kwargs):
    with open("parameters.json", "w") as file:
        json.dump(kwargs, file)
    kwargs["density"] = density
    trials = kwargs["trials"]
    print("running simulation for rho=%.2f" % density)
    stats = []
    actual_densities = []
    for i in range(trials):
        actual_density, data = run_model(**kwargs)
        stats.append(data)
        actual_densities.append(actual_density)
    density = np.mean(actual_densities)
    np.savez_compressed("CarRatio.%.2f.Density.%.2f" % (kwargs["car_ratio"], density), stats)

def run_model(**kwargs):
    RoadModel = PyRoad(**kwargs)
    RoadModel.initialize_layby(**kwargs)
    RoadModel.run(**kwargs)
    density = RoadModel.density
    return density, RoadModel.vehicle_stats
    
def simulation(virt, tau):
    parameters = base_parameters
    parameters.update({"num_virt_lanes": virt, "layby_transient": tau})
    base_folder_name = "virt_lanes.%d.tau.%d"
    folder = base_folder_name % (virt, tau)
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    densities = np.arange(0.05, 1, 0.05)
    with Pool(2) as p:
        p.map(partial(run_trials, **parameters), densities)
    

if __name__=="__main__":
    simulation(1, 1)
