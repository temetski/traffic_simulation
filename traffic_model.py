from pytraffic import PyRoad
import numpy as np
import os
import itertools
import json
from functools import partial
from multiprocessing import Pool, cpu_count

# the density resolution of this model is 0.01 for cars
base_parameters = {
    "num_lanes": 4,
    "len_road": 100,
#    "density": 0.1,
    "car_ratio": 1,
    "is_periodic": True,
    "timesteps": 1000,
    "p_lambda": 1,
    "num_virt_lanes": 1,
    "transient": 100,
    "layby_transient": 100,
    "trials": 100
}

def run_trials(density, **kwargs):
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
    np.savez_compressed("CarRatio.%.2f.Density.%.2f" % (kwargs["car_ratio"], density), data=stats)

def run_model(**kwargs):
    RoadModel = PyRoad(**kwargs)
    RoadModel.initialize_layby(**kwargs)
    RoadModel.run(**kwargs)
    density = RoadModel.density
    return density, RoadModel.vehicle_stats

def simulation(virt, tau):
    parameters = base_parameters.copy()
    parameters.update({"num_virt_lanes": virt, "layby_transient": tau})
    base_folder_name = "virt_lanes.%d.tau.%d"
    folder = base_folder_name % (virt, tau)
    if not os.path.exists(folder):
        os.makedirs(folder)
    os.chdir(folder)
    densities = np.concatenate((np.arange(0.04, 0.09, 0.03), np.arange(0.1, 0.3, 0.01), np.arange(0.3, 1, 0.05)))
    with open("parameters.json", "w") as file:
        json.dump(parameters, file)
    with Pool(cpu_count()//2 or 1) as p:
        p.map(partial(run_trials, **parameters), densities)
    os.chdir("../")

if __name__=="__main__":
    virts = [1, 2]
    taus = [100, 400, 700]
    simulation(0, 0)
    for virt, tau in itertools.product(virts, taus):
        simulation(virt, tau)
