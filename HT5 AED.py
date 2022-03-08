import simpy as sp
import random as rd
import numpy as np

class InitializeSimulation():
    def __init__(self,env,cpu=1,memory=100,speed=3):
        self.env = env
        self.cpu = sp.Resource(env,capacity = cpu)
        self.speed = speed
        self.RAM = sp.Container(env,init=memory,capacity=memory)
        self.waiting = sp.Resource(env,capacity=1)
                
def OperativeSystemSimulation(env,RAM,num,process,rand):
    # A new Process is created
    print(f'Process Number: {num} in NEW')
    # process requests for random number for memory
    memory = rand.randint(1,10)
    instructions = rand.randint(1,10)
    start = env.now
    #once program has memory assigned, is ready to be executed
    with RAM.RAM.get(memory) as READY:
        yield READY
        print(f'Process Number: {num} is READY')
        #until instructions are not over, program will run
        while(instructions > 0):
            with RAM.cpu.request() as RUNNING:
                yield RUNNING
                yield env.timeout(1)
                print(f'Process Number: {num} is RUNNING')
                instructions = instructions - RAM.speed
                
                if rand.randint(1,2)==2:
                    with RAM.waiting.request() as WAITING:
                        yield WAITING
                        print(f'Process Number: {num} is currently Waiting')
                        yield env.timeout(1)
                        
                    print(f'Process Number: {num} is READY')
                    
                    RAM.RAM.put(memory)
                    print(f'Process Number: {num} has been executed, current state: TERMINATED')
                    process.add(env.now-start)

class Stats():
    def __init__(self,total,cpu,memory,speed,time_interval):
        
        self.times = []
        self.total = total
        
    def add(self,item):
        self.times.append(item)
        
    def show(self):
        print(f'{self.total}\t{np.mean(self.times):2f}\t{np.std(self.times):2f}')
        

def RealTimeSimulation(memory=100,total_processes = 25,cpu=1,speed=3,time_interval = 10):
    env = sp.Environment()
    stats = Stats(total_processes,cpu,memory,speed,time_interval)
    RAM = InitializeSimulation(env,cpu,memory,speed)
    rand = rd.Random(123)
    num = 0
    total = total_processes
    
    for interval in range (1,25000):
        single_process = int(rand.expovariate(1.0/interval))
        for _ in range(single_process):
            env.process(OperativeSystemSimulation(env, RAM, num, stats, rand))
            num = num+1
            print(num)
            if num == total:
                break
        if num == total:
            break
        
        x = interval*time_interval
        env.run(x)
        
    env.run(env.now + 10000000000)
    return stats


list1 = []
for total_processes in [25,50,100,150,200]:
    list1.append(RealTimeSimulation(total_processes = total_processes))
    
print("A.")
print("Qty Avg     \tS.D")
for process in list1:
    process.show()
            