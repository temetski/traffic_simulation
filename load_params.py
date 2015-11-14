#! /usr/bin/python

import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'params.conf'
configParser.read(configFilePath)

ROADLENGTH = configParser.getint("params", "ROADLENGTH")
TRIALS = configParser.getint("params", "TRIALS")
REAL_LANES = configParser.getint("params", "REAL_LANES")
VIRTUAL_LANES = configParser.getint("params", "VIRTUAL_LANES")
SLOWDOWN = configParser.getfloat("params", "SLOWDOWN")
LANE_CHANGE_PROB = configParser.getfloat("params", "LANE_CHANGE_PROB")

