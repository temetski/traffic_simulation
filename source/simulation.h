#ifndef _SIMULATION_H
#define _SIMULATION_H

#if (_MSC_VER >= 1400)
#define _CRT_SECURE_NO_WARNINGS
#endif

#include "parameters.h"
#include "vehicles.h"
#include "road.h"

struct Simulation{
public:
	road_arr road;
	vector<Vehicle> vehicle_array;
	vector<int> throughput;
	vector<vector<vector<short> > > vehicle_data;
	int number_vehicles;
	Road *RoadModel;

	Simulation(void) {}
	~Simulation(void) {}

	void evolve(float density, float car_ratio);

private:
	void initialize(float density, float car_ratio);

};

void BZIP(char* _filename);

string start(float density, float car_ratio, time_t seed);

void animate(float density, float car_ratio, time_t seed);

void printstat(vector<string> status, vector<float> densities, float car_ratio);

#endif
