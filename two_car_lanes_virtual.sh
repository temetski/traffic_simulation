#! /bin/bash

#Script to be used with traffic_simulation.

export TRIALS=50
export TIMESTEPS=3000
export ROADLENGTH=50
export REAL_LANES=4
export VIRTUAL_LANES=1
export LANE_CHANGE=1

mkdir Two_Car_Lanes_Virtual
cd Two_Car_Lanes_Virtual

for car_ratio in "seq 0 0.05 1";
do
	../traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
done
