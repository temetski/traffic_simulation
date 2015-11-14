#! /bin/bash

#Script to be used with traffic_simulation.

export PATH=`pwd`:$PATH

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=100
REAL_LANES=4
SLOWDOWN=0.3
function run_sim {
	traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE -s $SLOWDOWN
}

function useparams {
        VIRTUAL_LANES=$1
        LANE_CHANGE=$2
        DIR='lanechange_'$LANE_CHANGE'_virt_'$VIRTUAL_LANES
        mkdir $DIR
        cd $DIR
        for car_ratio in `seq 0 0.25 1`;
        do
                run_sim
        done
        cd ..
}

#useparams 0 0.0
#useparams 0 0.1
#useparams 0 0.2
#useparams 0 0.3
#useparams 0 0.4
#useparams 0 0.5
#useparams 0 0.6
#useparams 0 0.7
#useparams 0 0.8
#useparams 0 0.9
#useparams 0 1.0



#useparams 1 0.1
#useparams 1 0.2
#useparams 1 0.3
#useparams 1 0.4
#useparams 1 0.5
#useparams 1 0.6
useparams 1 0.7
#useparams 1 0.8
#useparams 1 0.9
#useparams 1 1.0





