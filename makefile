CC = gcc
CPP = g++

CFLAGS  = -g -Wall -c -I/usr/include -fopenmp 
LFLAGS = -Wall -g -fopenmp -Wl,-rpath='$$ORIGIN' -L/usr/lib
# the build target executable:
TARGET = traffic_simulation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp
OBJS = traffic_simulation.o vehicles.o parameters.o


$(TARGET): $(OBJS)
	$(CPP) -std=c++11 $(LFLAGS) $(OBJS) -o $(TARGET) $(LIBS)

parameters.o: parameters.h parameters.cpp
	$(CPP) -std=c++11 $(CFLAGS) parameters.cpp $(LIBS)

vehicles.o: parameters.o vehicles.h vehicles.cpp
	$(CPP) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

traffic_simulation.o: hdf_save_compress.h vehicles.h traffic_simulation.cpp
	$(CPP) -std=c++11 $(CFLAGS) traffic_simulation.cpp $(LIBS)

clean:
	$(RM) $(TARGET) $(OBJS)
