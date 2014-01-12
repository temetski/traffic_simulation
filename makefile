# the compiler: gcc for C program, define as g++ for C++
CC = gcc

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -g -Wall -L/usr/lib -I/usr/include

# the build target executable:
TARGET = traffic_simulation

LIBS = -lgsl -lgslcblas -lhdf5 -lhdf5_cpp

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) -std=c++11 $(CFLAGS) -o $(TARGET) $(TARGET).cpp $(LIBS)

clean:
	$(RM) $(TARGET)