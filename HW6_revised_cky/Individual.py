#
# Individual.py
#
#

import math

#Base class for all individual types
#
class Individual:
    """
    Individual
    """
    minMutRate=1e-100
    maxMutRate=1
    learningRate=None
    uniprng=None
    normprng=None
    fitFunc=None

    def __init__(self):
        self.fit=self.__class__.fitFunc(self.state)
        self.mutRate=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma
            
    def mutateMutRate(self):
        self.mutRate=self.mutRate*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        if self.mutRate < self.minMutRate: self.mutRate=self.minMutRate
        if self.mutRate > self.maxMutRate: self.mutRate=self.maxMutRate
            
    def evaluateFitness(self):
        if self.fit == None: self.fit=self.__class__.fitFunc(self.state)
    
    



#A combinatorial integer representation class
#
class IntVectorIndividual(Individual):
    """
    IntVectorIndividual
    """
    nLength=None
    nItems=None
    mode = None
        
    def __init__(self):
        self.state=[]
        self.penalty = -self.nItems
        ### Initialization sould fit the 4th requirement.
        for i in range(self.nLength):
            a = self.uniprng.randint(0,self.nItems-1)
            self.state.append(a)

        if(self.mode == 1):     ### Construct the penalty value for constrained Tournaments
            self.panelty_value()

        if(self.mode == 2):
            self.repair()       ### repair the states
        
        
        super().__init__() #call base class ctor
        
    def crossover(self, other):
        #perform crossover "in-place"
        for i in range(self.nLength):
            if self.uniprng.random() < 0.5:
                tmp=self.state[i]
                self.state[i]=other.state[i]
                other.state[i]=tmp

        if(self.mode == 2):
            self.repair()       ### repair the states
                        
        self.fit=None
        other.fit=None
    
    def mutate(self):
        self.mutateMutRate()    #update mutation rate
        
        for i in range(self.nLength):
            if self.uniprng.random() < self.mutRate:
                self.state[i]=self.uniprng.randint(0,self.nItems-1)

        if(self.mode == 1):
            self.penalty=None

        if(self.mode == 2):
            self.repair()       ### repair the states
        
        self.fit=None
            
    def __str__(self):
        if self.mode ==1:
            return str(self.state)+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.mutRate +'\t' + str(self.penalty)
        else:
            return str(self.state)+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.mutRate
    
    def panelty_value(self):
        nItems_counts=0
        nList = list(range(0,self.nItems))
        penalty_value = -self.nItems
        
        for j in self.state:
            if j in nList:
                nItems_counts +=1
                nList.remove(j)
                penalty_value +=1
        self.penalty = penalty_value

    def repair(self):
        nItems_counts=0
        nList = list(range(0,self.nItems))
        for j in self.state:
            if j in nList:
                nItems_counts +=1
                nList.remove(j)
        maxItem = max(self.state,key=self.state.count)
        while (nItems_counts!= self.nItems):
            index_list = [k for k,item in enumerate(self.state) if item==maxItem]
            index = self.uniprng.sample(index_list,1)
            self.state[index[0]] = nList[0]
            nList.pop(0)
            nItems_counts += 1
    
    
#Multivariate real representation class
#
class MultivariateIndividual(Individual):
    """
    MultivariateIndividual
    """
    nLength=None
    minLimit=None
    maxLimit=None

    def __init__(self):
        self.state=[]
        for i in range(self.nLength):
            self.state.append(self.uniprng.uniform(self.minLimit,self.maxLimit))
         
        super().__init__() #call base class ctor
        
    def crossover(self, other):
        #perform crossover "in-place"
        alpha=self.uniprng.random()
        
        for i in range(self.nLength):
            tmp=self.state[i]*alpha+other.state[i]*(1-alpha)
            other.state[i]=self.state[i]*(1-alpha)+other.state[i]*alpha
            self.state[i]=tmp
            
            if self.state[i] > self.maxLimit: self.state[i]=self.maxLimit
            if self.state[i] < self.minLimit: self.state[i]=self.minLimit
            if other.state[i] > self.maxLimit: other.state[i]=self.maxLimit
            if other.state[i] < self.minLimit: other.state[i]=self.minLimit
        
        self.fit=None
        other.fit=None
    
    def mutate(self):
        self.mutateMutRate() #update mutation rate

        for i in range(self.nLength):
            self.state[i]=self.state[i]+(self.maxLimit-self.minLimit)*self.mutRate*self.normprng.normalvariate(0,1)
            if self.state[i] > self.maxLimit: self.state[i]=self.maxLimit
            if self.state[i] < self.minLimit: self.state[i]=self.minLimit
            
        self.fit=None
    
    def evaluateFitness(self):
        if self.fit == None: self.fit=self.__class__.fitFunc(self.state)
        
    def __str__(self):
        return str(self.state)+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.mutRate

