import pygame
from constants import fps

class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.fps = fps  

    def tick(self):
        return self.clock.tick(self.fps)
        
    def update(self):
        self.time_elapsed += self.clock.get_time()
        
    def reset(self):
        self.time_elapsed = 0
