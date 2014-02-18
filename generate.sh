#! /bin/bash

#Script to be used with traffic_simulation.

export PATH=`pwd`:$PATH

TRIALS=50
TIMESTEPS=3000
ROADLENGTH=50

function run_sim {
	traffic_simulation -c $car_ratio -T $TRIALS -t $TIMESTEPS -R $ROADLENGTH -r $REAL_LANES -v $VIRTUAL_LANES -L $LANE_CHANGE
}

function Two_Real {
	REAL_LANES=4
	VIRTUAL_LANES=0
	LANE_CHANGE=0
	DIR=Two_Real
	mkdir $DIR
	cd $DIR
	
	for car_ratio in `seq 0 0.05 1`;
        do
                run_sim
        done
        cd ..

}


function Single_Lane {
	REAL_LANES=1
	VIRTUAL_LANES=0
	LANE_CHANGE=0

	mkdir Single_Lane
	cd Single_Lane

	for car_ratio in `seq 0 0`;
	do
		run_sim
	done
	cd ..
}

function Two_Virtual {
	REAL_LANES=4
	VIRTUAL_LANES=1
	LANE_CHANGE=1

	mkdir Two_Car_Lanes_Virtual
	cd Two_Car_Lanes_Virtual

	for car_ratio in `seq 0 0.05 1`;
	do
		run_sim
	done
	cd ..
}

Two_Virtual
Two_Real
Single_Lane

