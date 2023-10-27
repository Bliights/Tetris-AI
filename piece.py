import pygame
from constants import shapes, gridWidth,gridHeight, colors, cellSize
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
                        (((self.y + j)* cellSize + (screen.get_width() - gridWidth* cellSize)//2) ,
                         ((self.x + i)* cellSize + (screen.get_height() - gridHeight* cellSize)//2),
                         cellSize,
                         cellSize,),
                    )
                    pygame.draw.rect(
                        screen, 
                        colors["black"], 
                        (((self.y + j)* cellSize + (screen.get_width() - gridWidth* cellSize)//2), 
                        ((self.x + i)* cellSize + (screen.get_height() - gridHeight* cellSize)//2), 
                        cellSize, 
                        cellSize), 
                        1
                    )
                    
    def draw_next_piece(self,screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        colors[self.colorName],
                        (((self.y + gridWidth*5//6 + j)* cellSize + (screen.get_width() - gridWidth* cellSize)//2) ,
                         ((self.x + gridHeight//5 + i)* cellSize + (screen.get_height() - gridHeight* cellSize)//2),
                         cellSize,
                         cellSize,),
                    )
                    pygame.draw.rect(
                        screen, 
                        colors["black"], 
                        (((self.y + gridWidth*5//6 + j)* cellSize + (screen.get_width() - gridWidth* cellSize)//2), 
                        ((self.x + gridHeight//5 + i)* cellSize + (screen.get_height() - gridHeight* cellSize)//2), 
                        cellSize, 
                        cellSize), 
                        1
                    )