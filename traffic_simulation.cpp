#if (_MSC_VER >= 1400)
	#define _CRT_SECURE_NO_WARNINGS
#endif

#include <iostream>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
#include <ctime>
#include <omp.h>

#include <fstream>
#include <bzlib.h>

#include "hdf_save_compress.h"
#include "vehicles.h"

using namespace std;

struct Simulation{
public:
	road_arr road;
	vector<vehicle> vehicle_array;
	vector<int> throughput;
	vector<vector<vector<int> > > vehicle_data;
	int number_vehicles;
	
	Simulation(void) {}
	~Simulation(void) {}

	void evolve(float density, float car_ratio){
		int passed_vehicles;
		initialize(density, car_ratio);
		vector<int> permutation(vehicle_array.size());
		throughput.resize(TIMESTEPS);
		for (unsigned i = 0; i < permutation.size(); i++) permutation[i] = i;
		random_shuffle(permutation.begin(), permutation.end());
		for (int t = 0; t < TIMESTEPS; t++){
			vector<vector<int> > vehicle_stats;
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
			for (vehicle vehicle : vehicle_array) vehicle_stats.push_back(vehicle.stats());
			vehicle_data.push_back(vehicle_stats);
			vector<vector<int> >().swap(vehicle_stats);
			random_shuffle(permutation.begin(), permutation.end());
		}
	}

private:
	void initialize(float density, float car_ratio){
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
			for (int i = 0; i < lane_choice.size(); i++) lane_choice[i] = i * 2;
			for (counter = 0; counter < number_car; counter++){
				int iterations = 0;
				pos = gsl_rng_uniform_int(generator, ROADLENGTH / 2) * 2 + 1;
				lane = lane_choice[gsl_rng_uniform_int(generator, 2)];
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
		//vector<vehicle>().swap(car_array);
		//vector<vehicle>().swap(moto_array);
	}

};

void BZIP(char* _filename){
	char message[100];
	sprintf(message, "bzip2 -6 %s", _filename);
	system(message);
}

string start(float density, float car_ratio){
	gsl_rng_set(generator, seed);
	time_t start = clock();
	vector<vector<vector<int> > > DATA;
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

void printstat(vector<string> status, vector<float> densities, float car_ratio){
#if (_WIN32)
	char clear[6] = "CLS";
#else
	char clear[8] = "clear";
#endif
	system(clear);
	for (int i = 0; i < 19; i++){
		cout << "Density::" << densities[i] << "\t\tCarRatio::" << car_ratio << "\t\tStatus:"<< status[i] << endl;
	}
}

static void show_usage(string name)
{
	std::cerr << "Usage: " << name << " -c CAR_RATIO [<option(s)> VALUES]\n"
		<< "Options:\n"
		<< "\t-h,--help\t\tShow this help message\n"
		<< "\t-c,--carratio\t\tSpecify the car ratio\n"
		<< "\t-T,--trials \t\tSpecify the number of trials (Default: " << TRIALS << ")\n"
		<< "\t-R,--roadlength \tSpecify the length of the road (Default: " << ROADLENGTH << ")\n"
		<< "\t-t,--timesteps \t\tSpecify the number of timesteps (Default: " << TIMESTEPS << ")\n"
		<< "\t-r,--reallanes \t\tSpecify the number of real lanes (Default: " << REAL_LANES << ")\n"
		<< "\t-v,--virtuallanes \tSpecify the number of virtual lanes (Default: " << VIRTUAL_LANES << ")\n"
		<< "\t-L,--lanechange \tToggle lane changing (Default: " << LANE_CHANGE << ")\n"
		<< endl;
}

int parser(int argc, char* argv[]){
	if (argc == 1) {
		cout << "Using default values." << endl;
		return 0;
	}
	for (int i = 1; i < argc; ++i) {
		std::string arg = argv[i];
		if ((arg == "-h") || (arg == "--help")) {
			show_usage(argv[0]);
			return 1;
		}
		else if ((arg == "-c") || (arg == "--carratio")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				car_ratio = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--carratio option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-T") || (arg == "--trials")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				TRIALS = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--trials option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-t") || (arg == "--timesteps")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				TIMESTEPS = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--timesteps option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-r") || (arg == "--reallanes")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				REAL_LANES = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
				LANES = REAL_LANES + VIRTUAL_LANES;
			}
			else {
				std::cerr << "--reallanes option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-v") || (arg == "--virtuallanes")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				VIRTUAL_LANES = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
				LANES = REAL_LANES + VIRTUAL_LANES;
			}
			else {
				std::cerr << "--virtuallanes option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-R") || (arg == "--roadlength")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				ROADLENGTH = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--roadlength option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-L") || (arg == "--lanechange")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				LANE_CHANGE = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--lanechange option requires one argument (0 or 1)." << std::endl;
				return 1;
			}
		}
	}
	return 0;
}

int main(int argc, char* argv[]){
	int status = parser(argc, argv);
	if (status == 1) return 1;

	vector<float> densities(19);
	vector<string> runmsg(19, "Not Done");
	double first = 0.05;
	for (int i = 0; i < 19; i++){
		densities[i] = first;
		first += 0.05;
	}
	int j = 4;
		omp_set_num_threads(2);
		#pragma omp parallel for
		for (int i = 0; i < densities.size(); i++){
			runmsg[i] = start(densities[i], car_ratio);
			printstat(runmsg, densities, car_ratio);
		}
	return 0;
}
