#include "vehicles.h"

gsl_rng * generator = gsl_rng_alloc(gsl_rng_mt19937);
time_t seed = time(NULL) * 123456789;

///* Debugging functions are contained here */
//void print_road(road_arr& array){
//	for (int i = 0; i < LANES; i++) {
//		for (int j = 0; j < ROADLENGTH; j++) {
//			printf("%d ", array[i][j]);
//		}
//		printf("\n");
//	}
//	printf("\n");
//}

void vehicle::place(road_arr& road){
	for (int _pos = (pos - length + ROADLENGTH + 1)%ROADLENGTH; _pos < (pos + 1); _pos++){
		for (int _lane = lane; _lane < lane + width; _lane++){
			road[_lane][_pos%ROADLENGTH] += marker;
		}
	}	
}

void vehicle::remove(road_arr& road){
	for (int _pos = (pos - length + ROADLENGTH + 1)%ROADLENGTH; _pos < (pos + 1); _pos++){
		for (int _lane = lane; _lane < lane + width; _lane++){
			road[_lane][_pos%ROADLENGTH] -= marker;
		}
	}
}

void vehicle::accelerate(void) {
	if (vel < V_MAX) vel += 1;
}

void vehicle::decelerate(road_arr& road) {
	int  count, _pos;
	_distance = V_MAX;
	for (int _lane = lane; _lane < lane + width; _lane++){
		_pos = pos + 1;
		count = 0;
		while ((road[_lane][_pos%ROADLENGTH] == 0) && (count < _distance)){
			_pos += 1;
			count += 1;
		}
		if (count < _distance) _distance = count; // least distance to vehicle infront
		//if (distance = 0) break;
	}
	if (_distance < vel) vel = _distance;
}

void vehicle::random_slow(void){
	double random = gsl_rng_uniform(generator);
	if (random < SLOWDOWN && vel > 0) vel -= 1;
}

void vehicle::move(road_arr& road){
	remove(road);
	pos = pos + vel;
	if (pos / ROADLENGTH == 1) {
		exit_road = true;
		pos = pos%ROADLENGTH;
	}
	else exit_road = false;
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
	int size = width * 3;
	int _pos, count, s;
	vector<int> headwaycount(size, 0);
	s = 0;
	for (int _lane = lane - width; s < size; _lane++){
		if (_lane >= 0 && _lane < LANES){
			_pos = pos + 1;
			count = 0;
			while (road[_lane][_pos%ROADLENGTH] == 0 && count < V_MAX){
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
	int center = (headwaycount.size() - 1) / 2;
	if (width > 1){
		for (unsigned i = 0; i < headwaycount.size() - 1; i++){
			headwaycount[i] = headwaycount[i] + headwaycount[i + 1];
		}
		center = distance(headwaycount.begin(), max_element(headwaycount.begin(), headwaycount.end()));
	}
	return center;
}

bool vehicle::check_lane(road_arr& road, int direction){
	if ((lane == 0 && direction == LEFT) || (lane == LANES - width && direction == RIGHT)) return false;
	for (int _pos = pos - length + 1; _pos < pos + vel + 1; _pos++){
		if (direction == LEFT && road[lane + direction][_pos%ROADLENGTH] != 0) return false;
		if (direction == RIGHT && road[lane + width][_pos%ROADLENGTH] != 0) return false;
	}
	return true;
}

void vehicle::change_lane(road_arr& road){
	vector<int> headcount;
	int center, _where;
	double probability;
	headcount = headway(road);
	center = (headcount.size() - 1) / 2;
	_where = aveheadway(headcount);
	/* Cars that have a higher chance to continue turning in the same direction*/
	if (lane > prev_lane) chance_right = 0.7;
	if (lane < prev_lane || lane == LANES - width) chance_right = 0.3;
	else chance_right = 0.5*LANE_CHANGE_PROB;
	probability = gsl_rng_uniform(generator);
	if (lane == LANES - width && vel>2 && VIRTUAL_LANES){
		if (check_lane(road, LEFT)){
			remove(road);
			lane += LEFT;
			place(road);
			prev_lane = lane;
			changed_lane = true;
		}
	}
	if (_distance <= vel && vel < V_MAX - 1){
		if (_where < center &&
			check_lane(road, LEFT) &&
			probability > LANE_CHANGE_PROB - chance_right){
			remove(road);
			lane += LEFT;
			place(road);
			prev_lane = lane;
			changed_lane = true;
		}
		if (_where > center &&
			check_lane(road, RIGHT) &&
			probability < chance_right){
			remove(road);
			lane += RIGHT;
			place(road);
			prev_lane = lane;
			changed_lane = true;
		}
		else changed_lane = false;
	}
	prev_lane = lane;
	changed_lane = false;
}

vector<int> vehicle::stats(void){
	vector<int> arr(2);
	arr = { vel, size };
	return arr;
}


bool place_check(int pos, int lane, int length, int width,
	road_arr& road, int ROADLENGTH){
	for (int _pos = (pos - length + 1); _pos < (pos + 1); _pos++){
		for (int _lane = lane; _lane < lane + width; _lane++){
			if (road[_lane][_pos%ROADLENGTH] != 0) return false;
		}
	}
	return true;
}