#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
#include <ctime>
#include "parameters.h"
#include "vehicles.h"

gsl_rng * generator = gsl_rng_alloc(gsl_rng_mt19937);
time_t seed = time(NULL) * 123456789;

vehicle::vehicle() {
	pos=0, lane=0, prev_lane=0, flag_slow=0;
	changed_lane=false;
	p_lambda=0;
}

void vehicle::mark(road_arr& road, short marker) {
	int _lengthcount = 0, roadlength=road[0].size();
	for (int _pos = (pos - length + 1)%roadlength; _lengthcount < length; _pos++){
        _lengthcount++;
		for (int _lane = lane; _lane < lane + width; _lane++){
			road[_lane][_pos%roadlength] += marker;
		}
	}
}

void vehicle::place(road_arr& road){
	mark(road, marker);
}

void vehicle::remove(road_arr& road){
	mark(road, -marker);
}

void vehicle::accelerate(void) {
	if (vel < V_MAX) vel += 1;
}

void vehicle::decelerate(road_arr& road) {
	distance(road);
	if (_distance < vel) vel = _distance;
}

void vehicle::distance(road_arr& road){
	int count, _pos, roadlength=road[0].size();
	_distance = V_MAX;
	for (int _lane = lane; _lane < lane + width; _lane++){
		_pos = pos + 1, count = 0;
		while ((road[_lane][_pos%roadlength] == 0) && (count < _distance)){
			_pos += 1, count += 1;
		}
		if (count < _distance) _distance = count; // least distance to vehicle infront
	}
}

void vehicle::random_slow(void){
	double random = gsl_rng_uniform(generator);
	if ( (random < SLOWDOWN) && (vel > 0) ) {vel -= 1; flag_slow=1;}
	else flag_slow=0;
}

void vehicle::move(road_arr& road, short dpos, short dlane, bool periodic){
	int roadlength=road[0].size();
	remove(road);
	pos = pos + dpos;
	lane = lane + dlane;
	if ((pos >= roadlength) && periodic) {
		pos = pos%roadlength;
	}
	if (!periodic && pos >= roadlength) pos = roadlength-1;
	place(road);
}

vector<int> vehicle::headway(road_arr& road){
	/*
	Counts the headway of the vehicle at its sides and in front.

	Returns
	-------
	Output: array
	3*width array of headway values.
	*/
	int size = width*3, roadlength=road[0].size(), lanes=road.size();
	int _pos, count, s;
	vector<int> headwaycount(size, 0);
	s = 0;
	for (int _lane = lane - width; s < size; _lane++){
		if ( (_lane >= 0) && (_lane < lanes) ){
			_pos = pos + 1;
			count = 0;
			while ( (road[_lane][_pos%roadlength] == 0) && (count < V_MAX) ){
				_pos += 1;
				count += 1;
			}
			headwaycount[s] = count;
		}
		s++;
	}
	return headwaycount;
}

int vehicle::aveheadway(vector<int>& headwaycount){
	int center;// = (headwaycount.size() - 1) / 2;
	if (width > 1){
		for (unsigned i = 0; i < headwaycount.size() - 1; i++){
			headwaycount[i] = headwaycount[i] + headwaycount[i + 1];
		}
	}
	center = std::distance(headwaycount.begin(), max_element(headwaycount.begin(), headwaycount.end()));
//    }
	return center;
}

bool vehicle::check_lane(road_arr& road, int direction){
	int roadlength=road[0].size(), lanes=road.size();
	if (( (lane == 0) && (direction == LEFT) ) || ( (lane == lanes - width) && (direction == RIGHT) )) return false;
	for (int _pos = pos - length + 1; _pos < pos + vel + 1; _pos++){
		if ( (direction == LEFT) && (road[lane + direction][_pos%roadlength] != 0) ) return false;
		if ( (direction == RIGHT) && (road[lane + width][_pos%roadlength] != 0) )  return false;
	}
	return true;
}

void vehicle::change_lane(road_arr& road, int num_virt_lanes){
	vector<int> headcount;
	int center, _where;
	double probability;
	headcount = headway(road);
	center = (headcount.size() - 1) / 2;
	_where = aveheadway(headcount);
	distance(road);
	probability = gsl_rng_uniform(generator);
    if (probability <= p_lambda){
	    // if ( (lane == (road.size() - width)) && (vel > 2) && num_virt_lanes ){
		//     if ( check_lane(road, LEFT) ){
		// 		move(road, 0, LEFT);
		// 	    changed_lane = true;
		//     }
	    // }
	    // else 
		if ( (_distance <= vel) && (vel < V_MAX) ){
		    if ( (_where < center) && check_lane(road, LEFT) ){
				move(road, 0, LEFT);
			    changed_lane = true;
		    }
		    else if ( (_where > center) && check_lane(road, RIGHT) ){
				move(road, 0, RIGHT);
			    changed_lane = true;
		    }
		    else changed_lane = false;
	    }
    }
    else {
	    changed_lane = false;
    }
	prev_lane = lane;
}

vector<short> vehicle::stats(void){
	vector<short> arr;
	arr = { pos, lane, vel, size, flag_slow };
	return arr;
}

bool place_check(int pos, int lane, int length, int width,
	road_arr& road, int roadlength){
    int _lengthcount = 0;
	for (int _pos = (pos - length + 1); _lengthcount < length; _pos++){
        _lengthcount++;
		for (int _lane = lane; _lane < lane + width; _lane++){
			if (road[_lane][_pos%roadlength] != 0) return false;
		}
	}
	return true;
}
