#
# Population.py
#
#

import copy
import math
from operator import attrgetter
from Individual2 import *

class Population:
    """
    Population
    """
    uniprng=None
    crossoverFraction=None
    mode=None
    
    def __init__(self, populationSize):
        """
        Population constructor
        """
        self.population=[]
        for i in range(populationSize):
            self.population.append(Individual())       
        
        
                                                                                                                               

    def __len__(self):
        return len(self.population)
    
    def __getitem__(self,key):
        return self.population[key]
    
    def __setitem__(self,key,newValue):
        self.population[key]=newValue
        
    def copy(self):
        return copy.deepcopy(self)
            
    def evaluateFitness(self):
        for individual in self.population: 
            individual.evaluateFitness()

            
    def mutate(self):     
        for individual in self.population:
            individual.mutate()
            
    def crossover(self):                            # Here self are whole population with [[lattice1],[lattice2],[lattice3]...]
        indexList1=list(range(len(self)))
        indexList2=list(range(len(self)))
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
            
        if self.crossoverFraction == 1.0:             
            for index1,index2 in zip(indexList1,indexList2):
                self[index1].crossover(self[index2])
        else:
            for index1,index2 in zip(indexList1,indexList2):
                rn=self.uniprng.random()
                if rn < self.crossoverFraction:
                    self[index1].crossover(self[index2])       
        
            
    def conductTournament(self):
        # binary tournament
        indexList1=list(range(len(self)))
        indexList2=list(range(len(self)))
        
        self.uniprng.shuffle(indexList1)
        self.uniprng.shuffle(indexList2)
        
        # do not allow self competition
        for i in range(len(self)):
            if indexList1[i] == indexList2[i]:
                temp=indexList2[i]
                if i == 0:
                    indexList2[i]=indexList2[-1]
                    indexList2[-1]=temp
                else:
                    indexList2[i]=indexList2[i-1]
                    indexList2[i-1]=temp

        #compete
        newPop=[]
        if self.mode==1:                                                #for conducting tournament for maximize fitness_value
            for index1,index2 in zip(indexList1,indexList2):
                if self[index1].fit > self[index2].fit:
                    newPop.append(copy.deepcopy(self[index1]))

                elif self[index1].fit < self[index2].fit:
                    newPop.append(copy.deepcopy(self[index2]))
                else:
                    rn=self.uniprng.random()
                    if rn > 0.5:
                        newPop.append(copy.deepcopy(self[index1]))
                    else:
                        newPop.append(copy.deepcopy(self[index2]))
        else:                                                          #for conducting tournament for minimize fitness_value
            for index1,index2 in zip(indexList1,indexList2):
                if self[index1].fit < self[index2].fit:
                    newPop.append(copy.deepcopy(self[index1]))

                elif self[index1].fit > self[index2].fit:
                    newPop.append(copy.deepcopy(self[index2]))
                else:
                    rn=self.uniprng.random()
                    if rn > 0.5:
                        newPop.append(copy.deepcopy(self[index1]))
                    else:
                        newPop.append(copy.deepcopy(self[index2]))

        
        # overwrite old pop with newPop    
        self.population=newPop        


    def combinePops(self,otherPop):
        self.population.extend(otherPop.population)
        

    def truncateSelect(self,newPopSize):
        if self.mode==0:
            self.population.sort(key=attrgetter('fit'),reverse=False)
        else:
            self.population.sort(key=attrgetter('fit'),reverse=True)
        self.population=self.population[:newPopSize]

    
    def print_show(self):
        best_fit_value=self.population[0].fit
        for individual in self.population:
            print(" x are: ", individual.x, "Fitness value:", individual.fit)
        if self.mode==0:
            for individual in self.population:
                if individual.fit < best_fit_value:
                    best_fit_value = individual.fit
        else:
            for individual in self.population:
                if individual.fit > best_fit_value:
                    best_fit_value = individual.fit
        print("Best_fit_value:",best_fit_value)
        
        
        

    def __str__(self):
        s=''
        for ind in self:
            s+=str(ind) + '\n'
        return s