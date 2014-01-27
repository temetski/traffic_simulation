#ifndef _VEHICLE_H
#define _VEHICLE_H

#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
#include <ctime>
#include "parameters.h"

using namespace std;

/* Program parameters are defined here */
#define RIGHT 1
#define LEFT -1

extern gsl_rng * generator;
extern time_t seed;

typedef vector<vector<int> > road_arr;

class vehicle {
public:
	int vel, pos, lane, width, length, marker, size, prev_lane = lane, _distance;
	bool changed_lane = false, exit_road = false;
	double chance_right;

private:
	vector<int> vehicle::headway(road_arr& road);
	int vehicle::aveheadway(vector<int>& headwaycount);
	bool vehicle::check_lane(road_arr& road, int direction);

public:
	void vehicle::place(road_arr& road);
	void vehicle::remove(road_arr& road);
	void vehicle::accelerate(void);
	void vehicle::decelerate(road_arr& road);
	void vehicle::random_slow(void);
	void vehicle::move(road_arr& road);
	void vehicle::change_lane(road_arr& road);
	vector<int> vehicle::stats(void);
};

class car : public vehicle{
public:
	car() { marker = 2, width = 2, length = 2, size = length*width; }
};

class motorcycle : public vehicle{
public:
	motorcycle() { marker = 1, width = 1, length = 1, size = length*width; }
};

bool place_check(int pos, int lane, int length, int width,
	road_arr& road, int ROADLENGTH);
#endif
