



import glob
import os
import string
folders = glob.glob("lanechange_*")

for i in folders:
    strings = i.split("_")
    paramtext = '''[params]
ROADLENGTH = 100
TRIALS = 50
REAL_LANES = 4
VIRTUAL_LANES = %s
SLOWDOWN = 0.3
LANE_CHANGE_PROB = %s''' % (strings[3], strings[1])
    os.chdir(i)
    text_file = open("params.conf", "w")
    text_file.write(paramtext)
    text_file.close()
    os.chdir("..")
