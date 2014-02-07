#! /bin/bash

#Script to be used with traffic_simulation.

export PATH = `pwd`:$PATH

function Two_Homo_Car {
	DIR=Two_Homo_Car
	cd $DIR
	plot_throughput.py
}

function Two_Homo_Motorcycle {
	DIR=Two_Homo_Motorcycle
	cd $DIR
	plot_throughput.py
}

function Single_Lane {
	mkdir Single_Lane
	cd Single_Lane
	plot_throughput.py
}

function Two_Virtual {
	mkdir Two_Car_Lanes_Virtual
	cd Two_Car_Lanes_Virtual
	plot_throughput.py
}

Two_Virtual
Two_Homo_Motorcycle
Two_Homo_Car
Single_Lane

