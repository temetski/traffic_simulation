# the compiler: gcc for C program, define as g++ for C++
CC = gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings

CFLAGS  = -g -Wall -c -I/usr/include -fopenmp 
LFLAGS = -Wall -g -fopenmp -Wl,-rpath='$$ORIGIN' -L/usr/lib
# the build target executable:
TARGET = traffic_simulation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp
OBJS = traffic_simulation.o vehicles.o parameters.o


$(TARGET): $(OBJS)
	$(CC) -std=c++11 $(LFLAGS) $(OBJS) -o $(TARGET) $(LIBS)

parameters.o: parameters.h parameters.cpp
	$(CC) -std=c++11 $(CFLAGS) parameters.cpp $(LIBS)

vehicles.o: parameters.o vehicles.h vehicles.cpp
	$(CC) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

traffic_simulation.o: hdf_save_compress.h vehicles.h traffic_simulation.cpp
	$(CC) -std=c++11 $(CFLAGS) traffic_simulation.cpp $(LIBS)


# gcc -Wl,-rpath,\$$ORIGIN/lib/ obj1.o obj2.o -o my_application
#vehicles.o: parameters.h  vehicles.h vehicles.cpp 
#	$(CC) -std=c++11 $(CFLAGS) vehicles.cpp $(LIBS)

clean:
	$(RM) $(TARGET) $(OBJS)
