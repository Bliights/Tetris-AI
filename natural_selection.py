import math

class Population:
    def __init__(self,size):
        self.ai = []
        self.fitnessSum = 0;
        self.bestAi
        self.generation = 1;
        
        self.batchSize = 16;
        self.currentBatchNumber = 0;
        self.numberOfBatches = math.ceil(size / self.batchSize);
        
