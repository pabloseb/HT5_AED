# Universidad del Valle de Guatemala
# Hoja de Trabajo 05

import simpy
import random


def process(name, env, arrive_time, cpu, ram,io):
    global total_time
    # get the time of initial_time with env.now()
    # yield for the arrive_time
    # calculate a random number of memory
    # ask for memory with ram.get(10)
    # calculate a random number of instructions between 1 and 10 with random.randint
    # while the instructions are not 0
        # yield for one unit of time with env.timetout(1)
        # subtract 3 to the instruction counter
        # create a random number between 1 and 2
        # if the number is 2 send the process to the waiting queue
            # ask for the resource of memory
            # yield between 1 and 3 units of time with env.timeout


    # when the instructions are less than 0 -> return the memory with  ram.get(10)
    # calculate the total time for this process = env.now() - initial_time
    # add the time to the total_time







# Defining the simulation environment
env = simpy.Environment()   # Main simpy environment
cpu = simpy.Resource(env, capacity=1)   # CPU resource (can take 3 instructions at a time)
io = simpy.Resource(env, capacity=1)
ram = simpy.Container(env, init=100, capacity=100)  # RAM container
random.seed(10) # Use the same seed for random

process_count = 25
total_time = 0

print("Simulando {} procesos".format(process_count))    # Print the number of processes to simulate

for i in range(process_count):
    env.process(process("proceso %d"%i, env, random.expovariate(1/10), cpu, ram, io))


env.run(50)





