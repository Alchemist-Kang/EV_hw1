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
    learningRate=1
    minLimit=None
    maxLimit=None
    uniprng=None
    normprng=None
    fitFunc=None
    get_key_func=None
    numParticleTypes=None
    latticeLength=None
    interactionEnergyMatrix=None
    selfEnergyVector=None


    def __init__(self):
        #setting dictionary of particle
        self.particle_types={}
        for j in range(self.numParticleTypes):
            if j==0:
                self.particle_types.update({'r':0})
            elif j==1:
                self.particle_types.update({'b':1})
            elif j==2:
                self.particle_types.update({'g':2})

        self.x=[self.uniprng.randrange(0,self.numParticleTypes) for _ in range(self.latticeLength)]
        self.fit=self.__class__.fitFunc(self.x, self.particle_types ,self.interactionEnergyMatrix, self.selfEnergyVector)
        self.key=self.__class__.get_key_func(self.particle_types,self.x)
        self.sigma=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma



        

        
    def crossover(self, other):
        #perform crossover "in-place"           here are self=[] , oter=[]  then do crossover create self'=[] , other'=[]

        alpha=self.uniprng.random()
        alpha=int(alpha*self.latticeLength)
        tmp1=self.x
        tmp2=other.x
        self.x=self.uniprng.sample(tmp1,alpha) + self.uniprng.sample(tmp2,(len(tmp2)-alpha))
        other.x=self.uniprng.sample(tmp2,alpha) + self.uniprng.sample(tmp2,(len(tmp2)-alpha))
        self.fit=None
        other.fit=None

 
    
    def mutate(self):
        self.sigma=self.sigma*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        if self.sigma < self.minSigma: self.sigma=self.minSigma
        if self.sigma > self.maxSigma: self.sigma=self.maxSigma
        max_value = self.numParticleTypes-1

        for idx,item in enumerate(self.x):
            item = int(item + (self.maxLimit-self.minLimit)*self.sigma*self.normprng.normalvariate(0,1))
            if item < 0:
                item = 0
            elif item > max_value:
                item = max_value
            self.x[idx]= item
        self.fit=None
        

        '''
        self.x=self.x+(self.maxLimit-self.minLimit)*self.sigma*self.normprng.normalvariate(0,1)
        self.fit=None
        '''
    
    def evaluateFitness(self):

        if self.fit == None: self.fit=self.__class__.fitFunc(self.x, self.particle_types, self.interactionEnergyMatrix, self.selfEnergyVector)

    def get_key(self):
        self.key=self.__class__.get_key_func(self.particle_types,self.x)

        
    def __str__(self):
        return '%0.8e'%self.x+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.sigma