#
# ev1.py: The simplest EA ever!
#
# To run: python ev1.py --input ev1_example.cfg
#         python ev1.py --input my_params.cfg
#
# Note: EV1 is fairly naive and has many fundamental limitations,
#           however, even though it's simple, it works!
#

import optparse
import sys
import yaml
import math
import matplotlib.pyplot as plt
import random
import numpy as np
from random import Random


#EV1 Config class 
class EV1_Config:
    """
    EV1 configuration class
    """
    # class variables
    sectionName='EV1'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'minLimit': (float,True),
             'maxLimit': (float,True),
             #'mutationProb': (float,True),
             #'mutationStddev': (float,True)
             }
     
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EC_Engine section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing EV1 section in cfg file')
         
        #iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval=eccfg[opt]
 
                #verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))
                 
                #create attributes on the fly
                setattr(self,opt,optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self,opt,None)
     
    #string representation for class data    
    def __str__(self):
        return str(yaml.dump(self.__dict__,default_flow_style=False))
         

#Simple 1-D fitness function example
#Now changing to a more complicated function
def fitnessFunc(x):
    return -10 -(0.04*x)*(0.04*x) + 10*np.cos(0.04*np.pi*x)

#Find index of worst individual in population
def findWorstIndex(l):
    minval=l[0].fit
    imin=0
    for i in range(len(l)):
        if l[i].fit < minval:
            minval=l[i].fit
            imin=i
    return imin


#Print some useful stats to screen
def printStats(pop,gen):
    print('Generation:',gen)
    avgval=0
    maxval=pop[0].fit
    for p in pop:
        avgval+=p.fit
        if p.fit > maxval: 
            maxval=p.fit
        print(str(p.x)+'\t'+str(p.fit))
    print('Max fitness',maxval)
    print('Avg fitness',avgval/len(pop))
    print('')

# Find Maximum Value and Return it
def maximum(pop,gen):
    max1=pop[0].fit
    state_v=pop[0].x
    for p in pop:
        if p.fit > max1:
            max1=p.fit
            state_v=p.x
    return max1, state_v

#Find Average Value and Return it
def avg_value(pop,gen):
    max1=pop[0].fit
    avg1=0
    avg=0
    for p in pop:
        avg1+=p.fit
    avg=avg1/(len(pop))
    return avg

#Find Std_values and Return it
def std_values(pop,gen):
    std_pop = []
    for p in pop:
        std_pop.append(p.fit)
    stddev_value = np.std(std_pop,ddof=1)

    return stddev_value



#A trivial Individual class     (changing of non-numerical part)
class Individual:
    def __init__(self,x=0,fit=0):
        self.x=x
        self.fit=fit

    def crossover(self,other):
        alpha = np.random.uniform(0.0,1.0)
        childx = alpha*self + (1-alpha)*other
        return Individual(childx,fitnessFunc(childx))
    
    def mutate(self):
        x_list=[]
        mutation_list=[]
        for p in self:
            x_list.append(p.x)
        original_std=np.std(x_list,ddof=1)
        tau = 1/(len(x_list)**(1/2))
        N = np.random.normal(0,1)
        new_std=original_std*np.exp(tau*N)
        if new_std > 2.0:
            new_std = 2.0
        elif new_std < -2.0:
            new_std = -2.0
        else:
            new_std = new_std

        for p in self:
            p.x = p.x + new_std*N
            mutation_list.append(p.x)
        
        return mutation_list


#EV1: The simplest EA ever!
#            
def ev1(cfg):
    # start random number generator         setting prng(pseudo random number generator) as Random()
    prng=Random()
    prng.seed(cfg.randomSeed)
    maxlist=[]
    best_list=[]
    state_values=[]
    average_list=[]
    std_list=[]

    #random initialization of population
    #Depeends on the populationSize to choose how many elements in list of population
    population=[]
    for i in range(cfg.populationSize):
        x=prng.uniform(cfg.minLimit,cfg.maxLimit)
        ind=Individual(x,fitnessFunc(x))
        population.append(ind)
        
    #print stats    
    printStats(population,0)
    maxlist = maximum(population,0)
    best_list.append(maxlist[0])
    state_values.append(maxlist[1])
    average_list.append(avg_value(population,0))
    std_list.append(std_values(population,0))
    
    


    #evolution main loop
    for i in range(cfg.generationCount):    #Do for i=0 ~ 49
        #self-adaptive mutation
        Individual.mutate(population)
        
        for j in range(5):
            parents=prng.sample(population,2)       #Randomly choose 2 parents each time while generatie a child
            child=Individual.crossover(parents[0].x,parents[1].x)   #Create 1 children 
            population.append(child)

        
        
        #Now we have 5 children with 10 parents in population, we only want no.1 to no.10 survive
        #All child_gen compete with parents and other children

        for k in range(5):
            iworst=findWorstIndex(population)
            population.pop(iworst)
        
        
        
        #print stats    
        printStats(population,i+1)
        maxlist = maximum(population,i+1)
        best_list.append(maxlist[0])
        state_values.append(maxlist[1])
        average_list.append(avg_value(population,i+1))
        std_list.append(std_values(population,i+1))
        
        

    #Plot Best fitness and state values  vs. generation count
    gcount = np.arange(0,16,1)
    plt.plot(gcount, best_list, linewidth=5, color="g", label = "BestFitness")
    plt.plot(gcount, state_values, linewidth=5, color="b", label = "State_values")
    plt.legend()
    plt.title("Best_fitness_and_State_value vs generation count")
    plt.savefig("Best_fitness_vs_gcount.png")
    plt.show()


    #Plot Average and standard deviation of population fitness vs. generation count
    plt.plot(gcount, average_list, linewidth=2, color="g", label="Avg_vs_gcount")
    plt.plot(gcount, std_list, linewidth=2, color="r", label="Std_vs_gcount")
    plt.legend()
    plt.title("Avg_Std vs generation count")
    plt.savefig("Avg_Std_vs_gcount.png")
    plt.show()




#
# Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        #
        # get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)
        
        #validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")
        
        #Get EV1 config params
        cfg=EV1_Config(options.inputFileName)
        
        #print config params
        print(cfg)
                    
        #run EV1
        ev1(cfg)
        
        if not options.quietMode:                    
            print('EV1 Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
    



# Plot the Fitness function
x = np.arange(-100,100,1)
y = -10 -(0.04*x)*(0.04*x) + 10*np.cos(0.04*np.pi*x)
plt.plot(x,y , linewidth=5, color="r")
plt.title("Fitness Function")
plt.savefig("Fitness_Function.png")
plt.show()




