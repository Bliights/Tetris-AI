from population import Population
import pygame

pygame.init()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

populationSize = 10
maxGeneration = 100
chanceToMutate = 0.1
gradedRetainPercent = 0.2
chanceRetainNongraded = 0.05
population = Population(populationSize,maxGeneration,chanceToMutate,gradedRetainPercent,chanceRetainNongraded,display)

while population.generation<population.maxGeneration and population.maxlineClear<5000:
    while population.isGenerationFinish()==False:
        population.update()
    population.naturalSelection()
    print(f'Max Lines clear : {population.maxlineClear} ({population.generation} generation)')

print(f"Solution found at generation n {population.generation}")
print(population.bestAi.multipliers)

pygame.quit()