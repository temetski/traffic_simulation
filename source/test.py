from pytraffic import PyRoad

parameters = {
    "num_lanes": 2,
    "len_road": 50,
    "density": 0.1,
    "car_ratio": 1,
    "is_periodic": True,
    "timesteps": 20,
    "p_lambda": 1,
    "num_virt_lanes": 0,
}
RoadModel = PyRoad(**parameters)
RoadModel.run(**parameters)
# RoadModel.layby_init()
# RoadModel.timestep(**parameters)
