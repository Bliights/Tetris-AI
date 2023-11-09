import pygame
from constants import fps

class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = fps  

    def tick(self):
        return self.clock.tick(self.fps)
