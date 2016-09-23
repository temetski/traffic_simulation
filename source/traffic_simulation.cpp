#if (_MSC_VER >= 1400)
#define _CRT_SECURE_NO_WARNINGS
#endif

#include <iostream>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <vector>
#include <algorithm> //random_shuffle, distance, max_element
#include <omp.h>
#include <fstream>
#include <bzlib.h>

#include "hdf_save.h"
#include "simulation.h"

using namespace std;

static void show_usage(string name)
{
	std::cerr << "Usage: " << name << " -c CAR_RATIO [<option(s)> VALUES]\n"
		<< "Options:\n"
		<< "\t-a,--animate\t\tAnimation mode\n"
		<< "\t--single\t\tSingle density mode\n"
		<< "\t-h,--help\t\tShow this help message\n"
		<< "\t-c,--carratio\t\tSpecify the car ratio\n"
		<< "\t-T,--trials \t\tSpecify the number of trials (Default: " << TRIALS << ")\n"
		<< "\t-R,--roadlength \tSpecify the length of the road (Default: " << ROADLENGTH << ")\n"
		<< "\t-t,--timesteps \t\tSpecify the number of timesteps (Default: " << TIMESTEPS << ")\n"
		<< "\t-r,--reallanes \t\tSpecify the number of real lanes (Default: " << REAL_LANES << ")\n"
		<< "\t-v,--virtuallanes \tSpecify the number of virtual lanes (Default: " << VIRTUAL_LANES << ")\n"
		<< "\t-f,--fractional \tSpecify the fraction of lane changing cars (Default: " << FRACTION_LANECHANGE << ")\n"
		<< "\t-L,--lanechange \tSet lane changing probability (Default: " << LANE_CHANGE_PROB << ")\n"
		<< "\t-s,--slowdown \tSet random slowdown probability (Default: " << SLOWDOWN << ")\n"
		<< "\t--loadseed \t\tSet seed state (Default: " << LOAD_SEED << ")\n"
		<< endl;
}

int parser(int argc, char* argv[]){
	if (argc == 1) {
		cout << "Using default values." << endl;
		return 0;
	}
	for (int i = 1; i < argc; ++i) {
		std::string arg = argv[i];
		if ((arg == "-h") || (arg == "--help")) {
			show_usage(argv[0]);
			return 1;
		}
		else if ((arg == "-c") || (arg == "--carratio")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				car_ratio = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--carratio option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-T") || (arg == "--trials")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				TRIALS = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--trials option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-t") || (arg == "--timesteps")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				TIMESTEPS = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--timesteps option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-r") || (arg == "--reallanes")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				REAL_LANES = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
				LANES = REAL_LANES + VIRTUAL_LANES;
			}
			else {
				std::cerr << "--reallanes option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-v") || (arg == "--virtuallanes")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				VIRTUAL_LANES = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
				LANES = REAL_LANES + VIRTUAL_LANES;
			}
			else {
				std::cerr << "--virtuallanes option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-R") || (arg == "--roadlength")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				ROADLENGTH = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--roadlength option requires one argument." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-f") || (arg == "--fractional")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				FRACTION_LANECHANGE = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--fractional option requires one argument (0 to 1)." << std::endl;
				return 1;
			}
		}
		else if ((arg == "-L") || (arg == "--lanechange")) {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				LANE_CHANGE_PROB = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--lanechange option requires one argument (0 to 1)." << std::endl;
				return 1;
			}
		}
		else if (arg == "--loadseed") {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				LOAD_SEED = atoi(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--loadseed option requires one argument (0 or 1)." << std::endl;
				return 1;
			}
		}
		else if (arg == "--single") {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				density = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--single option requires one argument (0 to 1)." << std::endl;
				return 1;
			}
		}
		else if (arg == "--slowdown" || arg == "-s") {
			if (i + 1 < argc) { // Make sure we aren't at the end of argv!
				i++;
				SLOWDOWN = atof(argv[i]); // Increment 'i' so we don't get the argument as the next argv[i].
			}
			else {
				std::cerr << "--slowdown option requires one argument (0 to 1)." << std::endl;
				return 1;
			}
		}
        else if (arg == "-a" || arg == "--animate") {
            ANIMATE = true;
		}
	}
	return 0;
}

int main(int argc, char* argv[]){
	int status = parser(argc, argv);
	if (status == 1) return 1;
	if (ANIMATE == true){
        int status = parser(argc, argv);
        if (status == 1) return 1;
        printf("Enter the desired density parameter:");
        float density;
        scanf("%f", &density);
        cout << density << car_ratio<<endl;
        if (LOAD_SEED == false) seed = time(NULL) * 123456789;
        animate(density, car_ratio, seed);
        char anim_py[100];
        sprintf(anim_py, "python animation.py --carratio %.2f --density %.2f --lanes %d", car_ratio, density, LANES);
        system(anim_py);
	}
	if (density != 0){
        int status = parser(argc, argv);
        if (status == 1) return 1;
        cout << density << car_ratio<<endl;
        if (LOAD_SEED == false) seed = 123456789;
        start(density, car_ratio, seed);
	}
    else{
    	vector<float> densities(99);
        vector<string> runmsg(99, "Not Done");
        double first = 0.01;
        for (int i = 0; i < 99; i++){
            densities[i] = first;
			first += 0.01;
        }
		omp_set_num_threads(omp_get_num_procs());
		#pragma omp parallel for
		for (int i = 0; i < densities.size(); i++){
			if (LOAD_SEED == false) seed = 123456789;
			runmsg[i] = start(densities[i], car_ratio, seed);
			printstat(runmsg, densities, car_ratio);
		}
    }
    return 0;
}
