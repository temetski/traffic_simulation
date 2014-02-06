#! /bin/bash

#Script to be used with traffic_simulation.

export PATH = `pwd`:$PATH

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=50

function Two_Homo_Car {
	REAL_LANES=4
	VIRTUAL_LANES=0
	LANE_CHANGE=0
	DIR=Homogenous/Two_Homo_Car
	mkdir -p $DIR
	cd $DIR

	car_ratio=1
	traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
}

function Two_Homo_Motorcycle {
	REAL_LANES=4
	VIRTUAL_LANES=0
	LANE_CHANGE=0
	DIR=Homogenous/Two_Homo_Motorcycle
	mkdir -p $DIR
	cd $DIR

	car_ratio=0
	traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
}

function Single_Lane {
	REAL_LANES=1
	VIRTUAL_LANES=0
	LANE_CHANGE=0

	mkdir Single_Lane
	cd Single_Lane

	for car_ratio in `seq 0 0`;
	do
		traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
	done
}

function Two_Virtual {
	REAL_LANES=4
	VIRTUAL_LANES=1
	LANE_CHANGE=1

	mkdir Two_Car_Lanes_Virtual
	cd Two_Car_Lanes_Virtual

	for car_ratio in `seq 0 0.05 1`;
	do
		traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
	done
}

Two_Virtual
Two_Homo_Motorcycle
Two_Homo_Car
Single_Lane

