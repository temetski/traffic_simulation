#! /bin/bash

#Script to be used with traffic_simulation.

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=50
REAL_LANES=4
VIRTUAL_LANES=0
LANE_CHANGE=0

DIR=Homogenous/Two_Homo_Motorcycle
mkdir -p $DIR
cd $DIR


car_ratio=0
../../traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE

