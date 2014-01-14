#! /bin/bash

#Script to be used with traffic_simulation.

export TRIALS=50
export TIMESTEPS=3000
export ROADLENGTH=50
export REAL_LANES=1
export VIRTUAL_LANES=0
export LANE_CHANGE=0

mkdir Single_Lane
cd Single_Lane

for car_ratio in "seq 0 0";
do
	../traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
done
