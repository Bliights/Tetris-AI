import pygame
from constants import fps,maxFps

class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.fps = fps  


    def tick(self):
        return self.clock.tick(self.fps)
    
    def acceleration(self):
        if fps<=maxFps:
            self.fps+=5
    
    def reset_speed(self):
        self.fps = fps
        
    def update(self):
        self.time_elapsed += self.tick()  

    def reset(self):
        self.time_elapsed = 0
