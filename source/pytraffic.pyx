# distutils: language = c++
# distutils: sources =

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool
import numpy as np

ctypedef vector[vector[int]] road_arr;

cdef extern from "vehicles.h":
    cdef cppclass vehicle:
        vehicle() except +
        short pos, lane, prev_lane, vel, flag_slow;
        short width, length, marker, size;
        bool changed_lane;
        double chance_right, p_lambda;
        # int _lengthcount;
        # vector[int] headway(road_arr& road);
        # int aveheadway(vector[int]& headwaycount);
        # bool check_lane(road_arr& road, int direction);
        void place(road_arr& road);
        void remove(road_arr& road);
        void accelerate();
        void decelerate(road_arr& road);
        void random_slow();
        void move(road_arr& road,short dpos, short dlane, bool periodic);
        void change_lane(road_arr& road, int num_virt_lanes);
        vector[short] stats();
    
    cdef cppclass car(vehicle):
        car() except +

    cdef cppclass motorcycle(vehicle):
        motorcycle() except +

cdef extern from "road.h":
    cdef cppclass Road:
        Road() except +
        Road(int len_road, int num_lanes, int num_virt_lanes, bool is_periodic) except +
        int lanes
        road_arr road;
        void timestep();
        void print_road();
        void initialize_periodic(float density, float car_ratio, float p_lambda);
        vector[vehicle] vehicle_array;

cdef class PyRoad:
    cdef Road cRoad
    cdef int len_road
    # cdef road_arr *road
    cdef vector[vehicle] *vehicle_array
    def __cinit__(self, **kwargs):
        self.len_road = kwargs["len_road"]
        self.cRoad = Road(kwargs["len_road"], kwargs["num_lanes"], kwargs["num_virt_lanes"], kwargs["is_periodic"])

    @property
    def road(self):
        return self.cRoad.road

    def layby_init(self):
        virt_lane = [9]*self.len_road
        virt_lane[6:8] = [0]*2
        self.cRoad.road.push_back(virt_lane)
        self.cRoad.lanes += 1
        # self.cRoad.print_road()
        print(self.cRoad.road)

    def run(self, **kwargs):
        self.cRoad.initialize_periodic(kwargs["density"], kwargs["car_ratio"], kwargs["p_lambda"])
        cdef int t
        for t in range(kwargs["timesteps"]):
            self.cRoad.timestep()
            self.cRoad.print_road()

    def timestep(self, **kwargs):
        self.cRoad.initialize_periodic(kwargs["density"], kwargs["car_ratio"], kwargs["p_lambda"])
        cdef int t, i, lanes, real_lanes
        lanes, real_lanes =  kwargs["num_lanes"] + kwargs["num_virt_lanes"], kwargs["num_virt_lanes"]
        vehicle_array = self.cRoad.vehicle_array
        for t in range(kwargs["timesteps"]):
            permutation = np.random.permutation(vehicle_array.size())
            for i in permutation:
                vehicle_array[i].accelerate();
                if (vehicle_array[i].p_lambda > 0):
                    vehicle_array[i].change_lane(self.cRoad.road, lanes-real_lanes);
                    vehicle_array[i].decelerate(self.cRoad.road);
                    if (not vehicle_array[i].changed_lane): 
                        vehicle_array[i].random_slow();
                    else: 
                        vehicle_array[i].flag_slow = 0;
                else:
                    vehicle_array[i].decelerate(self.cRoad.road);
                    vehicle_array[i].random_slow();
                vehicle_array[i].move(self.cRoad.road, vehicle_array[i].vel, 0, kwargs["is_periodic"]);
            self.cRoad.print_road()

    # def initialize_periodic(self, kwargs):
    #     density = kwargs["density"]
    #     car_ratio = kwargs["car_ratio"]
    #     p_lambda = kwargs["p_lambda"]
    #     cdef int pos, lane, counter;
    #     cdef float motor_ratio = 1 - car_ratio;
    #     cdef int number_vehicles = density*roadlength*(real_lanes) /
    #         (car().size*car_ratio + motorcycle().size*motor_ratio);
    #     cdef int number_car = car_ratio*number_vehicles;
    #     cdef int number_motorcycle;

    #     if (car_ratio > 0):
    #         lane_choice = [i*2 for i in range(lanes / car().width)]

    #         for counter in range(number_car):
    #             cdef int iterations = 0;
    #             pos = gsl_rng_uniform_int(generator, roadlength / 2) * 2 + 1;
    #             if (lane_choice.size() >= 2): lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
    #             else: lane = lane_choice[0];
    #             while (!place_check(pos, lane, car().length, car().width, road, roadlength)){
    #                 pos = gsl_rng_uniform_int(generator, roadlength / 2) * 2 + 1;
    #                 lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
    #                 if (iterations > 500): break;
    #                 iterations += 1;

    #             vehicle* b = vehicle_type[0]();
    #             vehicle_array.push_back(*b);
    #             vehicle_array.back().p_lambda = p_lambda;
    #             vehicle_array.back().pos = pos;
    #             vehicle_array.back().lane = lane;
    #             vehicle_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
    #             vehicle_array.back().place(road);

    #     if (motor_ratio > 0):
    #         number_motorcycle = number_vehicles - vehicle_array.size();
    #         for (counter = 0; counter < number_motorcycle; counter++):
    #             pos = 0;
    #             lane = 0;
    #             while (!place_check(pos, lane, motorcycle().length, motorcycle().width, road, roadlength)):
    #                 pos = gsl_rng_uniform_int(generator, roadlength);
    #                 lane = gsl_rng_uniform_int(generator, real_lanes);

    #             vehicle_array.push_back(motorcycle());
    #             vehicle_array.back().p_lambda = p_lambda;
    #             vehicle_array.back().pos = pos;
    #             vehicle_array.back().lane = lane;
    #             vehicle_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
    #             vehicle_array.back().place(road);
