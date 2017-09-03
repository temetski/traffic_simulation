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
	periodic = true;
};

Road::Road(int len_road, int num_lanes){
	roadlength = len_road;
	lanes = num_lanes;
    for (int i=0; i < lanes; i++) this->road.push_back(vector<int>(roadlength,0));
};

void Road::timestep(void){
    vector<int> permutation(vehicle_array.size());
    for (unsigned i = 0; i < permutation.size(); i++) permutation[i] = i;
    random_shuffle(permutation.begin(), permutation.end());
	vector<vector<short> > vehicle_stats;
	for (int i : permutation){
		vehicle_array[i].accelerate();
		if (vehicle_array[i].p_lambda > 0){
			vehicle_array[i].change_lane(road);
			vehicle_array[i].decelerate(road);
			if (!vehicle_array[i].changed_lane) vehicle_array[i].random_slow();
			else vehicle_array[i].flag_slow = 0;
		}
		else{
			vehicle_array[i].decelerate(road);
			vehicle_array[i].random_slow();
		}
		vehicle_array[i].move(road, vehicle_array[i].vel, 0);
	}
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

// void Road::move(road_arr& road, int dx, int dl){
//     int pos=2, lane=0;
// 	remove(road);
// 	pos = pos + dx;
//     lane = lane + dl;
// 	if (pos / roadlength == 1) {
// 		pos = pos%roadlength;
// 	}
// 	place(road);
// }

void Road::initialize_periodic(float density, float car_ratio){
    int pos, lane, counter;
    float motor_ratio = 1 - car_ratio;
    int number_vehicles = density*roadlength*(REAL_LANES) /
        (car().size*car_ratio + motorcycle().size*motor_ratio);
    int number_car = car_ratio*number_vehicles;
    int number_motorcycle;
    // RoadModel = new Road(roadlength, LANES);
    // vector<vehicle> car_array;
    /* Initializes Cars */
    if (car_ratio > 0){
        vector<int> lane_choice(lanes / car().width);
        for (unsigned i = 0; i < lane_choice.size(); i++) lane_choice[i] = i * 2;
        for (counter = 0; counter < number_car; counter++){
            int iterations = 0;
            pos = gsl_rng_uniform_int(generator, roadlength / 2) * 2 + 1;
			if (lane_choice.size() >= 2) lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
			else lane = lane_choice[0];
            while (!place_check(pos, lane, car().length, car().width, road, roadlength)){
				pos = gsl_rng_uniform_int(generator, roadlength / 2) * 2 + 1;
                lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
                if (iterations > 500) break;
                iterations += 1;
            }
            vehicle_array.push_back(car());
            vehicle_array.back().pos = pos;
            vehicle_array.back().lane = lane;
            vehicle_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            vehicle_array.back().place(road);
        }
    }
    /* Initializes Motorcycles */
    if (motor_ratio > 0){
        number_motorcycle = number_vehicles - vehicle_array.size();
        for (counter = 0; counter < number_motorcycle; counter++){
            pos = 0;
            lane = 0;
            while (!place_check(pos, lane, motorcycle().length, motorcycle().width, road, roadlength)){
                pos = gsl_rng_uniform_int(generator, roadlength);
                lane = gsl_rng_uniform_int(generator, REAL_LANES);
            }
            vehicle_array.push_back(motorcycle());
            vehicle_array.back().pos = pos;
            vehicle_array.back().lane = lane;
            vehicle_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            vehicle_array.back().place(road);
        }
    }
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