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
	short pos, lane, prev_lane = lane, _distance, width, length, marker, vel, size;
	bool changed_lane = false, exit_road = false;
	double chance_right;

private:
    int _lengthcount;
	vector<int> headway(road_arr& road);
	int aveheadway(vector<int>& headwaycount);
	bool check_lane(road_arr& road, int direction);

public:
	void place(road_arr& road);
	void remove(road_arr& road);
	void accelerate(void);
	void decelerate(road_arr& road);
	void random_slow(void);
	void move(road_arr& road);
	void change_lane(road_arr& road);
	vector<short> stats(void);
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
