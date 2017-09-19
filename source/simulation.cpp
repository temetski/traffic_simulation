#include "simulation.h"
#include "hdf_save.h"
#include <iostream>

int DATAPOINTS = 1000;


void Simulation::evolve(float density, float car_ratio){
    RoadModel = new Road(ROADLENGTH, LANES, true);
    RoadModel->initialize_periodic(density, car_ratio, LANE_CHANGE_PROB);
    for (int t = 0; t < TIMESTEPS; t++){
        vector<vector<short> > vehicle_stats;
        RoadModel->timestep(t);
        RoadModel->print_road();
        /* Eliminate the transient 2000 steps */
        if (t >= TIMESTEPS-DATAPOINTS){
			for (Vehicle vehicle : RoadModel->vehicle_array) {
				vehicle_stats.push_back(vehicle.stats());
			}
            vehicle_data.push_back(vehicle_stats);
            vector<vector<short> >().swap(vehicle_stats);
        }
    }
}


void Simulation::initialize(float density, float car_ratio){
    int pos, lane, counter;
    float motor_ratio = 1 - car_ratio;
    number_vehicles = density*ROADLENGTH*(REAL_LANES) /
        (Car().size*car_ratio + Motorcycle().size*motor_ratio);
    int number_car = car_ratio*number_vehicles;
    int number_motorcycle;
    RoadModel = new Road(ROADLENGTH, LANES);
    vector<Vehicle> car_array;
    /* Initializes Cars */
    if (car_ratio > 0){
        vector<int> lane_choice(LANES / Car().width);
        for (unsigned i = 0; i < lane_choice.size(); i++) lane_choice[i] = i * 2;
        for (counter = 0; counter < number_car; counter++){
            int iterations = 0;
            pos = gsl_rng_uniform_int(generator, ROADLENGTH / 2) * 2 + 1;
			if (lane_choice.size() >= 2) lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
			else lane = lane_choice[0];
            while (!place_check(pos, lane, Car().length, Car().width, RoadModel->road, ROADLENGTH)){
				pos = gsl_rng_uniform_int(generator, ROADLENGTH / 2) * 2 + 1;
                lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
                if (iterations > 500) break;
                iterations += 1;
            }
            car_array.push_back(Car());
            car_array.back().pos = pos;
            car_array.back().lane = lane;
            car_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            car_array.back().place(RoadModel->road);
        }
    }
    /* Initializes Motorcycles */
    if (motor_ratio > 0){
        number_motorcycle = number_vehicles - car_array.size();
        for (counter = 0; counter < number_motorcycle; counter++){
            pos = 0;
            lane = 0;
            while (!place_check(pos, lane, Motorcycle().length, Motorcycle().width, RoadModel->road, ROADLENGTH)){
                pos = gsl_rng_uniform_int(generator, ROADLENGTH);
                lane = gsl_rng_uniform_int(generator, REAL_LANES);
            }
            car_array.push_back(Motorcycle());
            car_array.back().pos = pos;
            car_array.back().lane = lane;
            car_array.back().vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            car_array.back().place(RoadModel->road);
        }
    }
    else vector<Vehicle> moto_array(0);
    /* Cleanup Operations */

    RoadModel->vehicle_array.swap(car_array);
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

void BZIP(char* _filename){
	char message[100];
	sprintf(message, "bzip2 -6 %s", _filename);
	system(message);
}


string start(float density, float car_ratio, time_t seed){
	gsl_rng_set(generator, seed);
	time_t start = clock();
	vector<vector<vector<short> > > DATA;
	char _filename[30];
	sprintf(_filename, "CarRatio.%.2f_Density.%.2f.h5", car_ratio, density);
	for (int trial = 1; trial < TRIALS + 1; trial++){
		Simulation *traffic = new Simulation;
		traffic->evolve(density, car_ratio);
		DATA = traffic->vehicle_data;
		delete traffic;
		hd5data(DATA, density, car_ratio, trial, _filename, seed);
	}
	BZIP(_filename);
	char message[30];
	sprintf(message, "done in %.3f seconds.", (clock() - start)*1.0 / (CLOCKS_PER_SEC));
	return message;
}

void animate(float density, float car_ratio, time_t seed){
	gsl_rng_set(generator, seed);
	vector<vector<vector<short> > > POS_DATA;
	char _filename[30];
	sprintf(_filename, "Animation_CR.%.2f_D.%.2f.h5", car_ratio, density);
	Simulation *traffic = new Simulation;
	traffic->evolve(density, car_ratio);
	POS_DATA = traffic->vehicle_data;
	delete traffic;
	hd5data(POS_DATA, density, car_ratio, 0, _filename, seed);
}

void printstat(vector<string> status, vector<float> densities, float car_ratio){
#if (_WIN32)
	char clear[6] = "CLS";
#else
	char clear[8] = "clear";
#endif
	system(clear);
	printf("plambda=%f, p_f=%f \n", LANE_CHANGE_PROB, SLOWDOWN);
	for (int i = 0; i < 99; i++){
		cout << "Density::" << densities[i] << "\t\tCarRatio::" << car_ratio << "\t\tStatus:" << status[i] << endl;
	}
}
