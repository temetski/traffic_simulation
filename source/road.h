#ifndef _ROAD_H
#define _ROAD_H

#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
// #include <ctime>
#include "parameters.h"
#include "vehicles.h"

using namespace std;

/* Program parameters are defined here */
#define RIGHT 1
#define LEFT -1

extern gsl_rng * generator;
extern time_t seed;

typedef vector<vector<int> > road_arr;

class Road {
public:
    road_arr road;
    int roadlength;
	int lanes;
	vector<vehicle> vehicle_array;

private:
	int periodic;

public:
	Road();
    Road(int len_road, int num_lanes);
	void timestep(void);
	void print_road();
	void initialize_periodic(float density, float car_ratio);
};

#endif
