#! /bin/bash

#Script to be used with traffic_simulation.

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=50
REAL_LANES=4
VIRTUAL_LANES=1
LANE_CHANGE=1

mkdir Two_Car_Lanes_Virtual
cd Two_Car_Lanes_Virtual

for i in `seq 0 0.05 1`;
do
	../traffic_simulation -c $i -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
done
