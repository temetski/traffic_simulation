# the compiler: gcc for C program, define as g++ for C++
CC = gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -g -Wall -c -L/usr/lib -I/usr/include -fopenmp
LFLAGS = -Wall -g -fopenmp
# the build target executable:
TARGET = traffic_simulation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp
OBJS = traffic_simulation.o vehicles.o


$(TARGET): $(OBJS)
	$(CC) -std=c++11 $(LFLAGS) $(OBJS) -o $(TARGET) $(LIBS)

vehicles.o: parameters.h  vehicles.h vehicles.cpp
	$(CC) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

traffic_simulation.o: hdf_save_compress.h vehicles.h traffic_simulation.cpp
	$(CC) -std=c++11 $(CFLAGS) traffic_simulation.cpp $(LIBS)

#vehicles.o: parameters.h  vehicles.h vehicles.cpp 
#	$(CC) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

clean:
	$(RM) $(TARGET) $(OBJS)
