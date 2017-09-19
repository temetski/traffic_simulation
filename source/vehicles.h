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

class Vehicle {
public:
	short pos, lane, prev_lane, vel, flag_slow, id;
	short width, length, marker, size;
	bool changed_lane;
	double chance_right, p_lambda;

private:
    int _lengthcount, _distance;
	void distance(road_arr& road);
	vector<int> headway(road_arr& road);
	int aveheadway(vector<int>& headwaycount);
	bool check_lane(road_arr& road, int direction);
	void mark(road_arr& road, short marker);


public:
	Vehicle();
	~Vehicle();
	void place(road_arr& road);
	void remove(road_arr& road);
	void accelerate(void);
	void decelerate(road_arr& road);
	void random_slow(void);
	void move(road_arr& road, short dpos=0, short dlane=0, bool periodic=true);
	void change_lane(road_arr& road, int num_virt_lanes=0);
	vector<int> stats(int time);
};

class Car : public Vehicle{
public:
	Car() { marker = 2, width = 2, length = 2, size = 4; }
};

class Motorcycle : public Vehicle{
public:
	Motorcycle() { marker = 1, width = 1, length = 1, size = 1; }
};

bool place_check(int pos, int lane, int length, int width,
	road_arr& road, int roadlength);

#endif
