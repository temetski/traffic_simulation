#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
// #include <ctime>
#include "parameters.h"
#include "vehicles.h"
#include "road.h"

Road::Road(){
};

Road::Road(int len_road, int num_lanes, int num_virt_lanes, bool is_periodic){
	periodic = is_periodic;
	roadlength = len_road;
	lanes = num_lanes + num_virt_lanes;
	real_lanes = num_lanes;
	id_tracker = 0;
    for (int i=0; i < lanes; i++) this->road.push_back(vector<int>(roadlength,0));
};

void Road::timestep(int t){
    vector<int> permutation(vehicle_array.size());
	vector<int> to_remove;
    for (unsigned i = 0; i < permutation.size(); i++) permutation[i] = i;
    random_shuffle(vehicle_array.begin(), vehicle_array.end());
	for (int i : permutation){
		vehicle_array[i].accelerate();
		if (vehicle_array[i].p_lambda > 0){
			vehicle_array[i].change_lane(road, lanes-real_lanes);
			vehicle_array[i].decelerate(road);
			if (!vehicle_array[i].changed_lane) vehicle_array[i].random_slow();
			else vehicle_array[i].flag_slow = 0;
		}
		else{
			vehicle_array[i].decelerate(road);
			vehicle_array[i].random_slow();
		}
		vehicle_array[i].move(road, vehicle_array[i].vel, 0, periodic);
		// if (!periodic) {
		// 	vehicle_array[i].remove(road);
		// 	to_remove.push_back(i);
		// }
		vehicle_stats.push_back(vehicle_array[i].stats(t));
	}
	// return vehicle_stats;
}

void Road::print_road(){
	for (int i = 0; i < lanes; i++) {
		for (int j = 0; j < roadlength; j++) {
			(road[i][j]>0) ? printf("%d", road[i][j]) : printf("_");
		}
		printf("\n");
	}
	printf("\n");
}

template <class X> Vehicle* make() {
  return new X;
}

void Road::initialize_periodic(float density, float car_ratio, float p_lambda){
    int pos, lane, counter;
    float motor_ratio = 1 - car_ratio;
    int number_vehicles = density*roadlength*(real_lanes) /
        (Car().size*car_ratio + Motorcycle().size*motor_ratio);
    int number_car = car_ratio*number_vehicles;
    int number_motorcycle;
    /* Initializes Cars */
    if (car_ratio > 0){
		number_car = place_vehicle_type((*make<Car>), number_car, p_lambda);
    }
    /* Initializes Motorcycles */
    if (motor_ratio > 0){
        number_motorcycle = number_vehicles - vehicle_array.size();
		number_motorcycle = place_vehicle_type((*make<Motorcycle>), number_motorcycle, p_lambda);
    }
	density = (number_motorcycle*Motorcycle().size+number_car*Car().size)/(roadlength*real_lanes);
    /* Cleanup Operations */

    // if (FRACTION_LANECHANGE<1.0){
    //     vector<int> permutation(vehicle_array.size());
    //     for (unsigned i = 0; i < permutation.size(); i++) permutation[i] = i;
    //     random_shuffle(permutation.begin(), permutation.end());
    //     int num_lanechanging = number_vehicles*FRACTION_LANECHANGE;
    //     counter = 0;
    //     for (int i : permutation){
    //       /* Assumes all vehicles are set to p_lambda=1 by default */
    //         if (counter>=num_lanechanging){
    //             vehicle_array[i].p_lambda = 0;
    //         }
    //         counter++;
    //     }
    // }
}

int Road::place_vehicle_type(Vehicle* (*veh_type)(), int number, float p_lambda){
	int pos, lane, counter;
	short width = veh_type()->width, length = veh_type()->length;
	vector<int> lane_choice(real_lanes / veh_type()->width);
	for (unsigned i = 0; i < lane_choice.size(); i++) lane_choice[i] = i * width;
	counter = 0;
	while (counter<number){
		int iterations = 0;
		pos = gsl_rng_uniform_int(generator, roadlength / length) * length + 1;
		if (lane_choice.size() >= 2) lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
		else lane = lane_choice[0];
		while (!place_check(pos, lane, length, width, road, roadlength)){
			pos = gsl_rng_uniform_int(generator, roadlength / 2) * 2 + 1;
			lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
			if (iterations > 500) break;
			iterations += 1;
		}
		vehicle_array.push_back(*veh_type());
		vehicle_array.back().p_lambda = p_lambda;
		vehicle_array.back().pos = pos;
		vehicle_array.back().lane = lane;
		vehicle_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
		vehicle_array.back().id = id_tracker;
		id_tracker++;
		vehicle_array.back().place(road);
		counter++;
	}
	return counter;
}