from pytraffic import PyRoad
import numpy as np
import os

trials = 50
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
}

def run_model(density):
    parameters["density"] = density
    RoadModel = PyRoad(**parameters)
    RoadModel.layby_init(**parameters)
    RoadModel.initialize_layby(**parameters)
    RoadModel.run(**parameters)
    density = RoadModel.density
    return RoadModel.vehicle_stats
    
def simulation(folder):
    os.chdir(folder)
    stats = []
    for density in np.arange(0.05, 1, 0.05):
        print("running simulation for rho=%.2f" % density)
        stats = [run_model(density) for i in range(trials)]
        np.savez("CarRatio.%.2f.Density.%.2f" % (parameters["car_ratio"], density), stats)

simulation("../layby_control")