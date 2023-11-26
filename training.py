from population import Population
import pygame
import concurrent.futures

pygame.init()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

populationSize = 30
maxGeneration = 100000
chanceToMutate = 0.1
gradedRetainPercent = 0.2
chanceRetainNongraded = 0.05
population = Population(populationSize,maxGeneration,chanceToMutate,gradedRetainPercent,chanceRetainNongraded,display)

while population.generation<population.maxGeneration and population.maxlineClear<1000:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(population.update,range(len(population.aiPopulation))) 
    population.naturalSelection()
    print(f'Max Lines clear : {population.maxlineClear} ({population.generation} generation)')

print(f"Solution found at generation n {population.generation}")
print(population.bestAi.multipliers)

pygame.quit()