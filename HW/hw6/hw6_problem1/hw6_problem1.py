#
# ev3.py: An elitist (mu+mu) generational-with-overlap EA
#
#
# To run: python ev3.py --input ev3_example.cfg
#         python ev3.py --input my_params.cfg
#
# Basic features of ev3:
#   - Supports self-adaptive mutation
#   - Uses binary tournament selection for mating pool
#   - Uses elitist truncation selection for survivors
#

import optparse
import sys
import yaml
import math
from random import Random
from Population import *
from Individual import Individual
from Population import Population


#EV3 Config class 
class EV3_Config:
    """
    EV3 configuration class
    """
    # class variables
    sectionName='EV3'
    options={'populationSize': (int,True),
             'generationCount': (int,True),
             'randomSeed': (int,True),
             'crossoverFraction': (float,True),
             'minLimit': (float,True),
             'maxLimit': (float,True),
             'numParticleTypes': (int,True),
             'latticeLength': (int,True),
             'selfEnergyVector': (list,True),
             'interactionEnergyMatrix': (list,True)}
     
    #constructor
    def __init__(self, inFileName):
        #read YAML config and get EV3 section
        infile=open(inFileName,'r')
        ymlcfg=yaml.safe_load(infile)
        infile.close()
        eccfg=ymlcfg.get(self.sectionName,None)
        if eccfg is None: raise Exception('Missing {} section in cfg file'.format(self.sectionName))
         
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
         

#Simple fitness function example: 1-D Rastrigin function
#        
def fitnessFunc(particle_series, particle_types ,interactionEnergyMatrix, selfEnergyVector):

    loss_value=0
    #self-energy
    for i in particle_series:
        loss_value = loss_value + selfEnergyVector[i]
    
    #interaction-energy with previous one
    for i in range(len(particle_series)):
        if i==0:
            loss_value=loss_value
        else:
            compare=get_key(particle_types, particle_series[i:i+1]) + get_key(particle_types, particle_series[i-1:i])
            if compare == ['r','r']:
                loss_value = loss_value + interactionEnergyMatrix[0][0]
            elif compare == ['r','b']:
                loss_value = loss_value + interactionEnergyMatrix[0][1]
            elif compare == ['r','g']:
                loss_value = loss_value + interactionEnergyMatrix[0][2]
            elif compare == ['b','r']:
                loss_value = loss_value + interactionEnergyMatrix[1][0]
            elif compare == ['b','b']:
                loss_value = loss_value + interactionEnergyMatrix[1][1]
            elif compare == ['b','g']:
                loss_value = loss_value + interactionEnergyMatrix[1][2]
            elif compare == ['g','r']:
                loss_value = loss_value + interactionEnergyMatrix[2][0]
            elif compare == ['g','b']:
                loss_value = loss_value + interactionEnergyMatrix[2][1]
            elif compare == ['g','g']:
                loss_value = loss_value + interactionEnergyMatrix[2][2]

    #interaction-energy with latter one
    for i in range(len(particle_series)-1):
        compare=get_key(particle_types, particle_series[i:i+2])
        if compare == ['r','r']:
            loss_value = loss_value + interactionEnergyMatrix[0][0]
        elif compare == ['r','b']:
            loss_value = loss_value + interactionEnergyMatrix[0][1]
        elif compare == ['r','g']:
            loss_value = loss_value + interactionEnergyMatrix[0][2]
        elif compare == ['b','r']:
            loss_value = loss_value + interactionEnergyMatrix[1][0]
        elif compare == ['b','b']:
            loss_value = loss_value + interactionEnergyMatrix[1][1]
        elif compare == ['b','g']:
            loss_value = loss_value + interactionEnergyMatrix[1][2]
        elif compare == ['g','r']:
            loss_value = loss_value + interactionEnergyMatrix[2][0]
        elif compare == ['g','b']:
            loss_value = loss_value + interactionEnergyMatrix[2][1]
        elif compare == ['g','g']:
            loss_value = loss_value + interactionEnergyMatrix[2][2]
    

    return loss_value


#Print some useful stats to screen
def printStats(pop,gen):
    print('Generation:',gen)
    pop.print_show()

def get_key(dict,list1):                #Send the particles of [0,1,0,2,0...] and changes to ['r','b','r','g','r',...] 
    keys=[]
    for i in list1:
        for key,values in dict.items():
            if values==i:
                keys.append(key)
        
    return keys




#EV3:
#            
def ev3(cfg):
    #start random number generators
    uniprng=Random()
    uniprng.seed(cfg.randomSeed)
    normprng=Random()
    normprng.seed(cfg.randomSeed+101)

    #set static params on classes
    # (probably not the most elegant approach, but let's keep things simple...)
    Individual.minLimit=cfg.minLimit
    Individual.maxLimit=cfg.maxLimit
    Individual.fitFunc=fitnessFunc
    Individual.get_key_func=get_key
    Individual.uniprng=uniprng
    Individual.normprng=normprng

    Individual.numParticleTypes=cfg.numParticleTypes
    Individual.latticeLength=cfg.latticeLength
    Individual.interactionEnergyMatrix=cfg.interactionEnergyMatrix
    Individual.selfEnergyVector=cfg.selfEnergyVector


    Population.uniprng=uniprng
    Population.crossoverFraction=cfg.crossoverFraction
      
    
    #create initial Population (random initialization)
    population=Population(cfg.populationSize)
        
    
    #print initial pop stats    
    printStats(population,0)
    

    
    #evolution main loop
    for i in range(cfg.generationCount):
        #create initial offspring population by copying parent pop
        offspring=population.copy()
        
        #select mating pool
        if i < 3:
            offspring.conductTournament()

        #perform crossover
        offspring.crossover()
        
        #random mutation
        offspring.mutate()
        
        #update fitness values
        offspring.evaluateFitness()   
        offspring.get_key()     
            
        #survivor selection: elitist truncation using parents+offspring
        population.combinePops(offspring)
        population.truncateSelect(cfg.populationSize)
        
        #print population stats    
        printStats(population,i+1)
    
        
        
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
        
        #Get EV3 config params
        cfg=EV3_Config(options.inputFileName)
        
        #print config params
        print(cfg)
                    
        #run EV3
        ev3(cfg)
        
        if not options.quietMode:                    
            print('EV3 Completed!')    
    
    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)
    

if __name__ == '__main__':
    main()
    