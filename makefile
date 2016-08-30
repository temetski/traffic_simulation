CC = gcc
CPP = g++

VPATH = source/
# optimization dapat ay -O2
CFLAGS  = -g -Wall -c -I/usr/include -I/usr/include/hdf5/serial -fopenmp
LFLAGS = -Wall -g -flto -fopenmp -Wl,-rpath='$$ORIGIN' -L/usr/lib
# the build target executable:
SIMULATION = traffic_simulation
ANIMATION = traffic_animation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp
OBJS = traffic_simulation.o vehicles.o parameters.o hdf_save.o simulation.o
OBJS2 = traffic_animation.o vehicles.o parameters.o hdf_save.o simulation.o

all: $(SIMULATION) #$(ANIMATION)
$(ANIMATION): $(OBJS2)
	$(CPP) -std=c++11 $(LFLAGS) $(OBJS2) -o $(ANIMATION) $(LIBS)

#traffic_animation.o: hdf_save.o vehicles.o simulation.o parameters.o traffic_animation.cpp
#	$(CPP) -std=c++11 $(CFLAGS) source/traffic_animation.cpp $(LIBS)

parameters.o: parameters.h parameters.cpp
	$(CPP) -std=c++11 $(CFLAGS) source/parameters.cpp $(LIBS)

vehicles.o: parameters.o vehicles.h vehicles.cpp
	$(CPP) -std=c++11 $(CFLAGS) source/vehicles.cpp $(LIBS)

hdf_save.o: hdf_save.cpp
	$(CPP) -std=c++11 $(CFLAGS) source/hdf_save.cpp $(LIBS)

simulation.o: simulation.h simulation.cpp
	$(CPP) -std=c++11 $(CFLAGS) source/simulation.cpp $(LIBS)

traffic_simulation.o: hdf_save.o vehicles.o simulation.o parameters.o traffic_simulation.cpp
	$(CPP) -std=c++11 $(CFLAGS) source/traffic_simulation.cpp $(LIBS)

clean:
	$(RM) $(SIMULATION) $(OBJS) $(ANIMATION) $(OBJS2)

