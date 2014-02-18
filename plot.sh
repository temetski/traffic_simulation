#! /bin/bash

#Script to be used with traffic_simulation.

export PATH=`pwd`:$PATH

function Two_Real {
	DIR=Two_Real
	cd $DIR
	plot_throughput.py
	cd ..
}

function Single_Lane {
	mkdir Single_Lane
	cd Single_Lane
	plot_throughput.py
	cd ..
}

function Two_Virtual {
	mkdir Two_Car_Lanes_Virtual
	cd Two_Car_Lanes_Virtual
	plot_throughput.py
	cd ..
}

Two_Virtual
Two_Real
Single_Lane

