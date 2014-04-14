#include "simulation.h"
#include "hdf_save.h"
#include <iostream>

int DATAPOINTS = 1000;


void Simulation::evolve(float density, float car_ratio){
    int passed_vehicles;
    initialize(density, car_ratio);
    vector<int> permutation(vehicle_array.size());
    throughput.resize(TIMESTEPS);
    for (unsigned i = 0; i < permutation.size(); i++) permutation[i] = i;
    random_shuffle(permutation.begin(), permutation.end());
    for (int t = 0; t < TIMESTEPS; t++){
        vector<vector<short> > vehicle_stats;
		vector<vector<short> > vehicle_pos_data;
        passed_vehicles = 0;
        for (int i : permutation){
            vehicle_array[i].accelerate();
            if (LANE_CHANGE){
                vehicle_array[i].change_lane(road);
                vehicle_array[i].decelerate(road);
                if (!vehicle_array[i].changed_lane) vehicle_array[i].random_slow();
            }
            else{
                vehicle_array[i].decelerate(road);
                vehicle_array[i].random_slow();
            }
            vehicle_array[i].move(road);
            if (vehicle_array[i].exit_road == true) passed_vehicles += 1;
        }
        /* Eliminate the transient 2000 steps */
        if (t >= TIMESTEPS-DATAPOINTS){
			for (vehicle vehicle : vehicle_array) {
				vehicle_stats.push_back(vehicle.stats());
			}
            vehicle_data.push_back(vehicle_stats);
            vector<vector<short> >().swap(vehicle_stats);
        }
        random_shuffle(permutation.begin(), permutation.end());
    }
}


void Simulation::initialize(float density, float car_ratio){
    int pos, lane, counter;
    float motor_ratio = 1 - car_ratio;
    number_vehicles = density*ROADLENGTH*(REAL_LANES) /
        (car().size*car_ratio + motorcycle().size*motor_ratio);
    int number_car = car_ratio*number_vehicles;
    int number_motorcycle;
    for (int i=0; i < LANES; i++) this->road.push_back(vector<int>(ROADLENGTH,0));
    vector<vehicle> car_array;
    /* Initializes Cars */
    if (car_ratio>0){
        vector<int> lane_choice(LANES / car().width);
        for (unsigned i = 0; i < lane_choice.size(); i++) lane_choice[i] = i * 2;
        for (counter = 0; counter < number_car; counter++){
            int iterations = 0;
            pos = gsl_rng_uniform_int(generator, ROADLENGTH / 2) * 2 + 1;
			if (lane_choice.size()>2) lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
			else lane = lane_choice[0];
            while (!place_check(pos, lane, car().length, car().width, road, ROADLENGTH)){
				pos = gsl_rng_uniform_int(generator, ROADLENGTH / 2) * 2 + 1;
                lane = lane_choice[gsl_rng_uniform_int(generator, lane_choice.size())];
                if (iterations > 500) break;
                iterations += 1;
            }
            car_array.push_back(car());
            car_array[counter].pos = pos;
            car_array[counter].lane = lane;
            car_array[counter].vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            car_array[counter].place(road);
        }
    }
    /* Initializes Motorcycles */
    if (motor_ratio > 0){
        number_motorcycle = number_vehicles - car_array.size();
        vector<vehicle> moto_array(number_motorcycle, motorcycle());
        for (counter = 0; counter < number_motorcycle; counter++){
            pos = 0;
            lane = 0;
            while (!place_check(pos, lane, motorcycle().length, motorcycle().width, road, ROADLENGTH)){
                pos = gsl_rng_uniform_int(generator, ROADLENGTH);
                lane = gsl_rng_uniform_int(generator, REAL_LANES);
            }
            moto_array[counter].pos = pos;
            moto_array[counter].lane = lane;
            moto_array[counter].vel = gsl_rng_uniform_int(generator, V_MAX + 1);
            moto_array[counter].place(road);
        }
        car_array.insert(car_array.end(), moto_array.begin(), moto_array.end());
    }
    else vector<vehicle> moto_array(0);
    /* Cleanup Operations */

    vehicle_array.swap(car_array);
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
	for (int i = 0; i < 19; i++){
		cout << "Density::" << densities[i] << "\t\tCarRatio::" << car_ratio << "\t\tStatus:" << status[i] << endl;
	}
}
