#! /bin/bash

#Script to be used with traffic_simulation.

export PATH=`pwd`:$PATH

function plot {
    VIRTUAL_LANES=$1
    LANE_CHANGE=$2
    DIR='lanechange_'$LANE_CHANGE'_virt_'$VIRTUAL_LANES
    echo "Processing folder: "$DIR
    cd $DIR
        python ../savedata.py
    cd ..
    echo "done folder: "$DIR >> log
}

#plot 0 0.0 &
#plot 0 0.1
#plot 0 0.2
#plot 0 0.3
#plot 0 0.4
plot 0 0.5
#plot 0 0.6
#plot 0 0.7
#plot 0 0.8
#plot 0 0.9
#plot 0 1.0



#plot 1 0.1
#plot 1 0.2
#plot 1 0.3
#plot 1 0.4
#plot 1 0.5
#plot 1 0.6
#plot 1 0.7
#plot 1 0.8
#plot 1 0.9
#plot 1 1.0

