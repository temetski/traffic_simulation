#! /bin/bash

#Script to be used with traffic_simulation.

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=50
REAL_LANES=1
VIRTUAL_LANES=0
LANE_CHANGE=0

mkdir Single_Lane
cd Single_Lane

for car_ratio in `seq 0 0`;
do
	../traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
done
