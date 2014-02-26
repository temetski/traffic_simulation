#ifndef _SIMULATION_H
#define _SIMULATION_H

#include "parameters.h"
#include "vehicles.h"

struct Simulation{
public:
	road_arr road;
	vector<vehicle> vehicle_array;
	vector<int> throughput;
	vector<vector<vector<int> > > vehicle_data;
	int number_vehicles;

	Simulation(void) {}
	~Simulation(void) {}

	void evolve(float density, float car_ratio);

private:
	void initialize(float density, float car_ratio);

};


#endif
