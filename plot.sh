#! /bin/bash

#Script to be used with traffic_simulation.

export PATH=`pwd`:$PATH

function plot {
    VIRTUAL_LANES=$1
    LANE_CHANGE=$2
    DIR='lanechange_'$LANE_CHANGE'_virt_'$VIRTUAL_LANES
    echo "Processing folder: "$DIR
    cd $DIR
	python ../plotter.py
    cd ..
}


export -f plot
SHELL=$(type -p bash) parallel -j 4 plot {1} {2} ::: 0 1 ::: 0.0 0.1 0.5 1.0

#plot 0 0.0
#plot 0 1.0
#plot 1 1.0
#plot 0 0.1
#plot 1 0.1
#plot 0 0.5
#plot 1 0.5
