from population import Population
import pygame
import concurrent.futures
import time


start_time = time.time()
pygame.init()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

populationSize = 100
maxGeneration = 10000
chanceToMutate = 0.1
gradedRetainPercent = 0.2
chanceRetainNongraded = 0.05
population = Population(populationSize,maxGeneration,chanceToMutate,gradedRetainPercent,chanceRetainNongraded,display)

while population.generation<population.maxGeneration and population.maxlineClear<10000:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(population.update,range(len(population.aiPopulation))) 
    population.naturalSelection()
    print(f'Max Lines clear : {population.maxlineClear} ({population.generation} generation)')

print(f"Solution found at generation n {population.generation}")
print(population.bestAi.multipliers)

pygame.quit()

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps d'exécution : {execution_time/60} minutes")