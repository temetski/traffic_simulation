/* Program parameters are defined here */
#include <vector>

using std::vector;

typedef vector<vector<int> > road_arr;
int ROADLENGTH = 50; //-R
int REAL_LANES = 4; //-r
int VIRTUAL_LANES = 1; //-v
int LANES = REAL_LANES + VIRTUAL_LANES;
int V_MAX = 5;
int TIMESTEPS = 100; //-t
int TRIALS = 1; //-T
float SLOWDOWN = 0.3;
float LANE_CHANGE_PROB = 0.8;
bool LANE_CHANGE = true;