# distutils: language = c++
# distutils: sources =

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool
import numpy as np

cdef int V_MAX
VMAX=5
ctypedef vector[vector[int]] road_arr;

cdef extern from "source/vehicles.h":
    cdef cppclass Vehicle:
        Vehicle() except +
        short pos, lane, prev_lane, vel, flag_slow, id;
        short width, length, marker, size;
        bool changed_lane;
        double chance_right, p_lambda;
        void place(road_arr& road);
        void remove(road_arr& road);
        void accelerate();
        void decelerate(road_arr& road);
        void random_slow();
        void move(road_arr& road,short dpos, short dlane, bool periodic);
        void change_lane(road_arr& road, int num_virt_lanes);
        vector[short] stats(int t);
    
    cdef cppclass Car(Vehicle):
        Car() except +

    cdef cppclass Motorcycle(Vehicle):
        Motorcycle() except +

    bool place_check(int pos, int lane, int length, int width,	road_arr& road, int roadlength)

cdef extern from "source/road.h":
    cdef cppclass Road:
        Road() except +
        Road(int len_road, int num_lanes, int num_virt_lanes, int trans_time, bool is_periodic) except +
        int lanes, real_lanes
        double density
        road_arr road;
        vector[vector[int]] vehicle_stats
        void timestep(int t);
        void print_road();
        void initialize_periodic(float density, float car_ratio, float p_lambda);
        vector[Vehicle] vehicle_array;
    
    Vehicle* make[T]();


cdef class PyRoad:
    cdef Road cRoad
    cdef Vehicle vehicle
    cdef vector[Vehicle] standby_array;
    cdef int len_road, lanes
    cdef vector[Vehicle] vehicle_array
    cdef id_tracker

    def __cinit__(self, **kwargs):
        self.len_road = kwargs["len_road"]
        self.lanes =  kwargs["num_lanes"] + kwargs["num_virt_lanes"]
        self.cRoad = Road(kwargs["len_road"], kwargs["num_lanes"], kwargs["num_virt_lanes"], 
                          kwargs["transient"], kwargs["is_periodic"])
        self.id_tracker = 0

    @property
    def road(self):
        return self.cRoad.road

    @property
    def density(self):
        return self.cRoad.density

    @property
    def vehicle_stats(self):
        return self.cRoad.vehicle_stats

    def run(self, **kwargs):
        cdef int t
        for t in range(-kwargs["transient"], kwargs["timesteps"]):
            self.cRoad.timestep(t)
            if t==kwargs["layby_transient"]:
                self.cRoad.vehicle_array.push_back(self.standby_array.back())

    def layby_init(self, **kwargs):
        length = self.len_road
        virt_lane = [9]*length
        virt_lane[length//2-1:length//2+1] = [0]*2
        for i in range(kwargs["num_virt_lanes"]):
            self.cRoad.road.push_back(virt_lane)
            self.cRoad.lanes += 1
        if kwargs["num_virt_lanes"]>0:
            self.vehicle = Car()
            self.standby_array.push_back(self.vehicle)
            self.standby_array.back().p_lambda = kwargs["p_lambda"];
            self.standby_array.back().pos = length//2;
            self.standby_array.back().lane = self.cRoad.lanes-2;
            self.standby_array.back().vel = 0;
            self.standby_array.back().place(self.cRoad.road);
            self.standby_array.back().id = self.id_tracker
            self.id_tracker += 1

    def initialize_layby(self, **kwargs):
        self.layby_init(**kwargs)
        cdef int roadlength = kwargs["len_road"];
        density = kwargs["density"]
        car_ratio = kwargs["car_ratio"]
        p_lambda = kwargs["p_lambda"]
        real_lanes = kwargs["num_lanes"]
        cdef int pos, lane, counter;
        cdef float motor_ratio = 1 - car_ratio;
        cdef int number_vehicles = density*roadlength*real_lanes / (Car().size*car_ratio + Motorcycle().size*motor_ratio);
        cdef int number_car = car_ratio*number_vehicles;
        if kwargs["num_virt_lanes"]>0: number_car -= 1
        cdef int number_motorcycle = 0;
        if (car_ratio > 0):
            number_car = self.place_vehicle_type("Car", number_car, p_lambda);
            if kwargs["num_virt_lanes"]>0: number_car += 1

        if (motor_ratio > 0):
            number_motorcycle = number_vehicles - self.cRoad.vehicle_array.size();
            number_motorcycle = self.place_vehicle_type("Motorcycle", number_motorcycle, p_lambda);
        size_car = number_car*Car().size
        size_moto = number_motorcycle*Motorcycle().size
        self.cRoad.density = float(size_car+size_moto)/(roadlength*real_lanes)

    cdef Vehicle make(self, veh_str):
        if veh_str==b"Car":
            return Car()
        elif veh_str==b"Motorcycle":
            return Motorcycle()

    cpdef int place_vehicle_type(self, char* veh_str, int number, float p_lambda):
        cdef Vehicle vehicle;
        vehicle = self.make(veh_str);
        cdef int pos, lane, counter, iterations;
        cdef int roadlength = self.len_road;
        cdef int real_lanes = self.cRoad.real_lanes;
        cdef vector[Vehicle] vehicle_array = self.cRoad.vehicle_array
        cdef short width = vehicle.width, length = vehicle.length;
        cdef vector[int] lane_choice;
        lane_choice = [i * width for i in range(real_lanes / width)];
        counter = 0
        while (counter<number):
            iterations = 0;
            pos = np.random.randint(roadlength / length) * length + 1;
            if (lane_choice.size() >= 2): lane = lane_choice[np.random.randint(lane_choice.size())];
            else: lane = lane_choice[0];
            while (not place_check(pos, lane, length, width, self.cRoad.road, roadlength)):
                pos = np.random.randint(roadlength / 2) * 2 + 1;
                lane = lane_choice[np.random.randint(lane_choice.size())];
                if (iterations > 500): break;
                iterations += 1;
            vehicle_array.push_back(self.make(veh_str));
            vehicle_array.back().p_lambda = p_lambda;
            vehicle_array.back().pos = pos;
            vehicle_array.back().lane = lane;
            vehicle_array.back().vel = np.random.randint(V_MAX + 1);
            vehicle_array.back().place(self.cRoad.road);
            vehicle_array.back().id = self.id_tracker
            self.id_tracker += 1
            counter += 1
        self.cRoad.vehicle_array = vehicle_array
        return counter