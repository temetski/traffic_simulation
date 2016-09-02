#include "parameters.h"

int ROADLENGTH = 50; //-R
int REAL_LANES = 1; //-r
int VIRTUAL_LANES = 0; //-v
int LANES = REAL_LANES + VIRTUAL_LANES;
int V_MAX = 5;
int TIMESTEPS = 3000; //-t
int TRIALS = 50; //-T
double SLOWDOWN = 0.3;
double LANE_CHANGE_PROB = 0.4;
double car_ratio = 0;
bool LANE_CHANGE = true;
bool LOAD_SEED = false;
bool ANIMATE = false;
