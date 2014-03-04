CC = gcc
CPP = g++

CFLAGS  = -g -Wall -c -I/usr/include -fopenmp
LFLAGS = -Wall -g -fopenmp -Wl,-rpath='$$ORIGIN' -L/usr/lib
# the build target executable:
SIMULATION = traffic_simulation
ANIMATION = traffic_animation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp
OBJS = traffic_simulation.o vehicles.o parameters.o hdf_save.o simulation.o
OBJS2 = traffic_animation.o vehicles.o parameters.o hdf_save.o simulation.o

all: $(SIMULATION) $(ANIMATION)
$(SIMULATION): $(OBJS)
	$(CPP) -std=c++11 $(LFLAGS) $(OBJS) -o $(SIMULATION) $(LIBS)

$(ANIMATION): $(OBJS2)
	$(CPP) -std=c++11 $(LFLAGS) $(OBJS2) -o $(ANIMATION) $(LIBS)

traffic_animation.o: hdf_save.o vehicles.o simulation.o parameters.o traffic_animation.cpp
	$(CPP) -std=c++11 $(CFLAGS) traffic_animation.cpp $(LIBS)

parameters.o: parameters.h parameters.cpp
	$(CPP) -std=c++11 $(CFLAGS) parameters.cpp $(LIBS)

vehicles.o: parameters.o vehicles.h vehicles.cpp
	$(CPP) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

hdf_save.o: hdf_save.h hdf_save.cpp
	$(CPP) -std=c++11 $(CFLAGS) hdf_save.cpp $(LIBS)

simulation.o: simulation.h simulation.cpp
	$(CPP) -std=c++11 $(CFLAGS) simulation.cpp $(LIBS)

traffic_simulation.o: hdf_save.o vehicles.o simulation.o parameters.o traffic_simulation.cpp
	$(CPP) -std=c++11 $(CFLAGS) traffic_simulation.cpp $(LIBS)

clean:
	$(RM) $(SIMULATION) $(OBJS) $(ANIMATION) $(OBJS2)

