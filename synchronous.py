#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy.random as randstate


###########################################################################
#   Define the kinds of vehicles as Classes
###########################################################################

class Vehicle():
    '''Parent Class.'''
    def __init__(self, width, length, marker):
        self.vel = 0
        self.pos = 0
        self.lane = 0
        self.width = width
        self.length = length
        self.size = self.length*self.width
        self.type = "Kotse"
        self.prev_lane = 0
        self.chance_right = 0.5
        self.marker = marker

    def place(self, road, ROADLENGTH):
        for i in xrange(self.pos-self.length+1, self.pos+1):
            road[self.lane:self.lane+self.width, i % ROADLENGTH] = self.marker
        return road

    def remove(self, road, ROADLENGTH):
        for i in xrange(self.pos-self.length+1, self.pos+1):
            road[self.lane:self.lane+self.width, i % ROADLENGTH] = 0
        return road

    def move(self, road, ROADLENGTH):
        through = 0
        if self.pos+self.vel > ROADLENGTH:
            through = 1
        road = self.remove(road, ROADLENGTH)
        self.pos = (self.pos+self.vel) % ROADLENGTH
        road = self.place(road, ROADLENGTH)
        return road, through

class Car(Vehicle):
    def __init__(self):
        Vehicle.__init__(self, 2, 2, 1)

class Motorcycle(Vehicle):
    def __init__(self):
        Vehicle.__init__(self, 1, 1, 2)



def acceleration(vehicle):## 1
    '''Adds 1 to the current velocity of the selected vehicle.

    Accelerates vehicle when it is not yet at maximum velocity. The limit
    to the velocity is defined by the variable V_MAX.'''
    vehicle.vel += vehicle.vel < V_MAX
    return vehicle


def deceleration(vehicle, road, ROADLENGTH):## 2
    '''Reduces the speed of the selected vehicle.

    The speed is reduced when the distance between the selected vehicle
    and the closest vehicle in front of it is less than the velocity of
    the selected vehicle. If so, the selected vehicle will have its speed
    reduced to the distance.'''
    dist = distance_check(vehicle, road, ROADLENGTH)
    if vehicle.vel > dist:
        vehicle.vel = dist
    return vehicle


def random_slow(vehicle, slowdown_probability):## 3
    '''Reduces the speed of the vehicle by 1.

    Introduces a probability of randomly slowing down a vehicle.The slowdown
    probabilities are fixed for each vehicle.'''
    if vehicle.lane == NUMBER_LANES - vehicle.width and vehicle.vel>2:
        vehicle.vel = 2
    elif vehicle.vel > 0:
        vehicle.vel -= randstate.uniform() < slowdown_probability
    return vehicle


def distance_check(vehicle, road, ROADLENGTH):
    pos, lane = vehicle.pos+1, vehicle.lane
    distance = 0
    while (all(road[lane:lane+vehicle.width, pos%ROADLENGTH] == 0)
           and distance<V_MAX):
        distance += 1
        pos += 1
    return distance


def headway(vehicle, road, ROADLENGTH):
    '''Counts the headway of the vehicle at its sides and in front.

    Returns
    -------
    Output: ndarray
        3*width array of headway values.'''
    lane, pos = vehicle.lane, vehicle.pos
    width, length = vehicle.width, vehicle.length
    left, right = 0, width
    for r in xrange(2):
        if (lane+right+width)<(NUMBER_LANES):
            right += width
        else:
            right += (NUMBER_LANES - (lane+right))
            break
    for l in xrange(2):
        if lane+left-width >= 0:
            left -= width
        else:
            left -= (lane+left)%width
            break
    headwaycount = np.zeros(right-left)
    pos_counter = pos+1
    condition = road[lane+left:lane+right, pos_counter %ROADLENGTH] == 0
    while any(condition) and pos_counter<(V_MAX*2+pos):
        pos_counter += 1
        headwaycount += condition
        condition *= road[lane+left:lane+right, pos_counter %ROADLENGTH] == 0
    if left > -2*width:
        headwaycount = np.insert(headwaycount, 0, np.zeros(2*width+left))
    if lane >=  NUMBER_LANES - 2*width -1:
        headwaycount = np.append(headwaycount, np.zeros(3*width-right))
    return headwaycount


def aveheadway(vehicle, headwaycount):
    center = len(headwaycount-1)/2
    width = vehicle.width
    lcr = [np.mean(headwaycount[i:i+width])
        for i in xrange(len(headwaycount)-width+1)]
    whichlane = np.where(lcr == max(lcr))[0]
    if center not in whichlane:
        return randstate.choice(whichlane)
    elif randstate.uniform(1)<0.4:
        return randstate.choice(whichlane)
    else:
        return center


def check_right_lane(vehicle, road, ROADLENGTH):
    lane, pos, vel = vehicle.lane, vehicle.pos %ROADLENGTH, vehicle.vel
    width, length = vehicle.width, vehicle.length
    if lane ==  NUMBER_LANES - width:
        return False
    for i in xrange(pos-length+1, pos+vel+1):
        if road[lane+width, i % ROADLENGTH] != 0:
            return False
    return True


def check_left_lane(vehicle, road, ROADLENGTH):
    lane, pos, vel = vehicle.lane, vehicle.pos %ROADLENGTH, vehicle.vel
    length = vehicle.length
    if lane == 0:
        return False
    for i in xrange(pos-length+1, pos+vel+1):
        if road[lane-1, i % ROADLENGTH] != 0:
            return False
    return True


def lane_change(vehicle, road, ROADLENGTH):
    lane = vehicle.lane
    vel = vehicle.vel
    length, width = vehicle.length, vehicle.width
    headcount = headway(vehicle, road, ROADLENGTH)
    center = (len(headcount)-1)/2
    where = aveheadway(vehicle, headcount)
    ## Cars that have a higher chance to continue turning in the same direction
    if lane > vehicle.prev_lane:
        vehicle.chance_right = 0.7
    elif lane < vehicle.prev_lane or lane == NUMBER_LANES-width:
        vehicle.chance_right = 0.3
    else:
        vehicle.chance_right = 0.5*LANECHANGE_PROB
    p = randstate.uniform()
    if lane == NUMBER_LANES-width and vel>2:
        if check_left_lane(vehicle, road, ROADLENGTH):
            vehicle.remove(road, ROADLENGTH)
            vehicle.lane -= 1
            vehicle.place(road, ROADLENGTH)
            vehicle.prev_lane = lane
            return road, True
    elif distance_check(vehicle, road, ROADLENGTH)<=vel and vel<V_MAX-1:
        if where < center and check_left_lane(vehicle, road,
                    ROADLENGTH) and p > LANECHANGE_PROB - vehicle.chance_right:
            vehicle.remove(road, ROADLENGTH)
            vehicle.lane -= 1
            vehicle.place(road, ROADLENGTH)
            vehicle.prev_lane = lane
            return road, True
        elif where > center and check_right_lane(vehicle, road,
                            ROADLENGTH) and p < vehicle.chance_right:
            vehicle.remove(road, ROADLENGTH)
            vehicle.lane += 1
            vehicle.place(road, ROADLENGTH)
            vehicle.prev_lane = lane
            return road, True
        else: return road, False
    vehicle.prev_lane = lane
    return road, False


def initialize(density, car_ratio, ROADLENGTH):
    iterations = 0
    motor_ratio = 1 - car_ratio
    number_vehicles = int((density*ROADLENGTH*REAL_LANES)/
                  (Car().size*car_ratio + Motorcycle().size*motor_ratio))
    number_car = int(car_ratio*number_vehicles)
    number_motorcycle = number_vehicles - number_car
    car_array = np.array([Car() for i in xrange(number_car)] +
                [Motorcycle() for i in xrange(number_motorcycle)])
    road = np.zeros([NUMBER_LANES, ROADLENGTH], dtype=np.uint8)
    car_lane_choice = range(NUMBER_LANES-1)[::2]
###########################################################################
#   initializes the cars
###########################################################################
    length = Car().length
    for i in xrange(number_car):
        if iterations < 100:
            iterations += 1
        else:
            iterations = 0
            car_array = np.delete(car_array, np.s_[i:number_car])
            number_vehicles -= number_car-i
            number_car -= number_car-i
            break
        car_array[i].pos = randstate.randint(ROADLENGTH/2)*2 + 1
        car_array[i].lane = randstate.choice(car_lane_choice)
        while not place_check(car_array[i], road, ROADLENGTH):
            car_array[i].pos = (car_array[i].pos+length)%ROADLENGTH
            car_array[i].lane = randstate.choice(car_lane_choice)
        car_array[i].place(road, ROADLENGTH)
        car_array[i].vel = randstate.randint(V_MAX)
###########################################################################
#   initializes motorcycles
###########################################################################
    length = Motorcycle().length
    for i in xrange(number_car, number_car+number_motorcycle):
        car_array[i].pos = randstate.randint(ROADLENGTH)
        car_array[i].lane = randstate.randint(NUMBER_LANES-1)
        while not place_check(car_array[i], road, ROADLENGTH):
            if car_array[i].pos < ROADLENGTH:
                car_array[i].pos += length
            else:
                car_array[i].pos = randstate.randint(ROADLENGTH)
                car_array[i].lane = randstate.randint(NUMBER_LANES-1)
        car_array[i].place(road, ROADLENGTH)
        car_array[i].vel = randstate.randint(V_MAX)
    #slowdown_probability = randstate.beta(6, 4, number_vehicles - 1)
    slowdown_probability = np.array([0.3]*(number_vehicles-1))
    slowdown_probability = np.insert(slowdown_probability, 0, 0)
    return car_array, road, slowdown_probability, number_vehicles


def place_check(vehicle, road, ROADLENGTH):
    lane, pos = vehicle.lane, vehicle.pos
    width, length = vehicle.width, vehicle.length
    for i in xrange(pos-length+1, pos+1):
        if any(road[lane:lane+width, i%ROADLENGTH] != 0):
            return False
    return True


def evolve(density, car_ratio, ROADLENGTH, seedstate=None):
    '''Returns array containing positions of tracer car for each timestep.

    Returns
    -------
    Output: ndarray
        Array of all the displacements of the tracer vehicle.'''
    if seedstate:
        global randstate
    randstate = np.random.RandomState(seedstate)
    car_array, road, slowdown_probability, number_vehicles = \
                initialize(density, car_ratio, ROADLENGTH)
    if not car_array[0].type == ID:
        car_array = np.insert(car_array, 0, car_array[-1])
        car_array = np.delete(car_array, -1)
    car_array[0].marker = 3
    permutation = range(number_vehicles)
    randstate.shuffle(permutation)
    throughput = []
    vehicles = [car_array]
    for t in xrange(TIMESTEPS):
        passed_cars = 0
        for i in permutation:
            car_array[i] = acceleration(car_array[i])
            car_array[i] = deceleration(car_array[i], road, ROADLENGTH)
            road, Change = lane_change(car_array[i], road, ROADLENGTH)
            if not Change:
                car_array[i] = random_slow(car_array[i],
                                    slowdown_probability[i])
#            car_array[i] = random_slow(car_array[i], slowdown_probability[i])
            road, through = car_array[i].move(road, ROADLENGTH)
            passed_cars += through
        throughput.append(passed_cars)
        randstate.shuffle(permutation)
        vehicles.append(car_array)
    return vehicles, throughput



def load_seed(filename):
    seed = np.load(filename)['seed']
    return int(seed)

CHANGING = False
LANECHANGE_PROB = 0.8
REAL_LANES = 4
VIRTUAL_LANES = 1
NUMBER_LANES = REAL_LANES + VIRTUAL_LANES
ROADLENGTH = 50
TRIALS =  1
TIMESTEPS = 3000
V_MAX = 5
ID = "Kotse"
LOAD = False

def main_routine(car_ratio):
    import time
    start = time.time()

    for density in [0.5]:#np.arange(0.8, 0.9, 0.1):
        print 'car_ratio = ', car_ratio, ';\t RoadDensity = ', density
        vehicles = []
        throughput = []
        for i in xrange(TRIALS):
#            if LOAD == True:
#                seeder = load_seed("Kos.npz" % car_ratio)
#            else:
#                seeder = np.random.randint(1234567890)
            seeder = np.random.randint(1234567890)
            data, through = evolve(density, car_ratio,
                                      ROADLENGTH, seedstate=seeder)
            vehicles.append(data)
            throughput.append(through)

#        np.savez_compressed("FT.%slane.T%s.RL%s.r%sd%s" %
#                 (NUMBER_LANES, TRIALS, ROADLENGTH, car_ratio, density),
#                 vehicles=vehicles, throughput=throughput, seeder=seeder)

    end = time.time()
    print end - start
    return 0


if __name__ == '__main__':
#    pool = Pool(2)
#    pool.map(main_routine, np.arange(0.1, 0.2, 0.1))
    main_routine(0)



