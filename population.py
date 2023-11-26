from ai import Ai
from random import randint,random,choice

class Population:
    def __init__(self,
                 populationSize,
                 maxGeneration,
                 chanceToMutate,
                 gradedRetainPercent,
                 chanceRetainNongraded,
                 screen
                 ):
        
        self.populationSize = populationSize
        self.aiPopulation = []
        for i in range(self.populationSize):
            newAi=Ai(screen)
            newAi.randomizeMultipliers()
            newAi.game.status.set_solo()
            self.aiPopulation.append(newAi)
        
        self.maxGeneration = maxGeneration
        self.generation = 0;
        self.chanceToMutate = chanceToMutate
        self.gradedRetainPercent = gradedRetainPercent 
        self.chanceRetainNongraded = chanceRetainNongraded 
        
        self.gradedIndividualCount = (int)(self.populationSize*self.gradedRetainPercent)
        
        self.bestAi = Ai(screen)
        self.maxlineClear = 0
        
    def update(self):
        for i in range(self.populationSize):
            if self.aiPopulation[i].game.status.is_solo() and self.aiPopulation[i].game.totaLinesClear<5000:
                if(len(self.aiPopulation[i].movementPlan)==0):
                    self.aiPopulation[i].addMoves(self.aiPopulation[i].getBestMove())
                self.aiPopulation[i].nextMove()
                self.aiPopulation[i].game.update_gravity()
        
    def isGenerationFinish(self):
        finish = True
        for i in range(self.populationSize):
            if self.aiPopulation[i].game.status.is_solo() and self.aiPopulation[i].game.totaLinesClear<5000:
                finish = False
        return finish
    
    def calculateAiFitnesses(self): 
        for i in range(self.populationSize): 
            self.aiPopulation[i].calculateFitness()
    
    def populationSortedByFitness(self):
        self.aiPopulation = sorted(self.aiPopulation, key=lambda x: x.fitness, reverse=True)
        
    
    def setBestAi(self):
        self.bestAi = self.aiPopulation[0];
        for i in range(self.populationSize): 
            if (self.aiPopulation[i].fitness>self.bestAi.fitness):
                self.bestAi=self.aiPopulation[i]
    
    def createParents(self):
        parents = self.aiPopulation[:self.gradedIndividualCount]
        for individual in self.aiPopulation[self.gradedIndividualCount:]:
            if random() < self.chanceRetainNongraded:
                parents.append(individual)
        self.aiPopulation = parents
        for i in range(len(self.aiPopulation)):
            self.aiPopulation[i].reset()
        return parents
    
    def populationMutation(self):
        for i in range(len(self.aiPopulation)):
            self.aiPopulation[i].mutate(self.chanceToMutate)
        
    def createChildren(self,father,mother):
        children = father.clone()
        children.reset()
        for key, value in father.multipliers.items():
            children.multipliers[key]=(father.multipliers[key]+mother.multipliers[key])/2
        return children
            
    def naturalSelection(self):
        self.calculateAiFitnesses()
        self.populationSortedByFitness()
        self.setBestAi()
        self.maxlineClear=self.bestAi.game.totaLinesClear
        
        self.createParents()
        self.populationMutation()
        
        childrenNumber = self.populationSize - len(self.aiPopulation)
        children = []
        while len(children) < childrenNumber:
            father = choice(self.aiPopulation)
            mother = choice(self.aiPopulation)
            if father!=mother:
                children.append(self.createChildren(father,mother))
        
        self.aiPopulation.extend(children)
        self.generation+=1
        
        