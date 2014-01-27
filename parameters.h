#ifndef _PARAMETERS_H
#define _PARAMETERS_H

/* Program parameters are defined here */
#include <vector>

using std::vector;


extern int ROADLENGTH; //-R
extern int REAL_LANES; //-r
extern int VIRTUAL_LANES; //-v
extern int LANES;
extern int V_MAX;
extern int TIMESTEPS; //-t
extern int TRIALS; //-T
extern double SLOWDOWN;
extern double LANE_CHANGE_PROB;
extern double car_ratio;
extern bool LANE_CHANGE;
extern bool LOAD_SEED;

#endif
