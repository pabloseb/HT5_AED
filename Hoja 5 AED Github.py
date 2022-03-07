# Universidad del Valle de Guatemala
# Hoja de Trabajo No.5
# Pablo Herrera || Guillermo Santos || Jorge Andrino

# Goal: Simulate a program execution of a operative system with shared time

#first: a new program is created and asks for a random amount of memory between 1-10
#if there is space in memory, program runs if not it needs to wait
#if program runs, it executes 3 instructions at a time for a limited time and then it is terminated

import simpy as sp
import random as rd
import statistics as st


class MemorySimulation(object):
    def __init__(self,env,CPU=1):
        self.env = env
        self.CPU = sp.Resource(env,capacity=CPU)
        self.RandomAccessMemory = sp.Container(env,init=100,capacity=100)
        self.Instructions = 3
        self.Wait = sp.Resource(env,capacity=1)

class Statistics():
    def __init__(self,total,processors,memory,instructions,intervals):
        self.times = []
        self.title = "Processes"+{total}+" processors "+{processors}+" Memory "+{memory}+" Instructions Taken"+{instructions}+" time intervals"+{intervals}
        self.total = total
        
    def addLast(self, element):
        self.times.append(element)
        
    def titles(self):
        print("\n"+ self.title)
        print("Avg\tStandard Deviation")
        print({st.mean(self.times)}+"\t"+{st.stdev(self.times)})
        
    def stats(self):
        print({self.total}+"\t"+{st.mean(self.times)}+"\t"+{st.stdev(self.times)})
        
        
def SingleProcess(env,ram,process_number,process,random):
    print("Process No."+{process_number}+" has been created")
    memory = random.randint(1,10)
    instructions = random.randint(1,10)
    start = env.now
    with ram.RandomAccessMemory.get(memory) as Ready:
        yield Ready
        print("Process No."+{process_number}+"Is Ready")
        while(instructions > 0):
            with ram.CPU.request() as Running:
                yield Running
                print("Process No."+{process_number}+"is Running")
                instructions = instructions - ram.Instructions
                
                if random.randint(1,2)==2:
                    with ram.Wait.request() as Waiting:
                        yield Waiting
                        print("Process No."+{process_number}+"is currently Waiting")
                        yield env.timeout(1)
                        
                print("Process No."+{process_number}+"Is Ready")
            ram.RandomAccessMemory.put(memory)
            print("Process No."+{process_number}+"has been Terminated")
            process.add(env.now - start)
            
def Simulation(memory=100,total_processes = 25, processors = 1, instructions = 3, interval_time = 10):
    env = sp.Environment()
    processes = Statistics(total_processes,processors,memory,instructions,interval_time)
    ram = MemorySimulation(env,processors)
    random = rd.Random(123)
    
    numbers = 0
    total = total_processes
    
    for interval in range(1,25000):
        x = int(random.expovariate(1.0/interval))
        for _ in range(x):
            env.process(SingleProcess(env,ram,numbers,processors,random))
            numbers = numbers + 1
            print(numbers)
            if numbers == total:
                break
        if numbers == total:
            break
        
        env.run(interval*interval_time)
        return processes
            
            