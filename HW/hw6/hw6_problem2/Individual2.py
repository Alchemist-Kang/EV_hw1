#
# Individual.py
#
#

import math

#A simple 1-D Individual class
class Individual:
    """
    Individual
    """
    minSigma=1e-100
    maxSigma=1
    learningRate=1/(2**(1/2))
    minLimit=None
    maxLimit=None
    uniprng=None
    normprng=None
    fitFunc=None

    def __init__(self):

        self.x=[self.uniprng.uniform(-5.12,5.12) for _ in range(2)]
        self.fit=self.__class__.fitFunc(self.x)
        self.sigma=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma
        
    def crossover(self, other):
        #perform crossover "in-place"           here are self=[] , oter=[]  then do crossover create self'=[] , other'=[]

        alpha=self.uniprng.random()
        for i in range(len(self.x)):
            self.x[i]=self.x[i]*alpha + other.x[i]*(1-alpha)
            other.x[i]=other.x[i]*alpha + self.x[i]*(1-alpha)

        self.fit=None
        other.fit=None
        

 
    
    def mutate(self):
        self.sigma=self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma
        

        for idx,item in enumerate(self.x):
            item = item + self.sigma*self.normprng.normalvariate(0,1)
            if item < self.minLimit:
                item = self.minLimit
            elif item > self.maxLimit:
                item = self.maxLimit
            self.x[idx] = item
            
        self.fit=None

    
    def evaluateFitness(self):

        if self.fit == None: self.fit=self.__class__.fitFunc(self.x)


        
    def __str__(self):
        return '%0.8e'%self.x+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.sigma