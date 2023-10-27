import pygame
from constants import shapes, gridWidth, colors, cellSize
from random import choice

class Piece:
    def __init__(self):
        self.shape = choice(shapes) 
        self.x = 0
        self.y = (gridWidth)//2 - len(self.shape[0])//2
        pieceColors = {color: rgb for color, rgb in colors.items() 
                       if color not in ["black", "white"]}
        self.colorName = choice(list(pieceColors.keys()))
    
    
    def draw_piece(self,screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        colors[self.colorName],
                        ((self.y + j) * cellSize,
                         (self.x + i) * cellSize,
                         cellSize,
                         cellSize,),
                    )
                    pygame.draw.rect(
                        screen, 
                        colors["black"], 
                        ((self.y + j) * cellSize, 
                        (self.x + i) * cellSize, 
                        cellSize, 
                        cellSize), 
                        1
                    )