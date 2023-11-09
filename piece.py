import pygame
from constants import shapes, color_per_shape, gridWidth, colors, cellSize
from random import randint

class Piece:
    
    def __init__(self):
        random = randint(0,len(shapes)-1)
        self.shape = shapes[random]
        # coordinate of the piece(top left corner of the piece)
        self.x = (gridWidth)//2 - len(self.shape[0])//2
        self.y = 0
        
        self.color = color_per_shape[random]
    
    # Move the piece one square to the left
    def move_left(self):
        self.x -= 1
    
    # Move the piece one square to the right
    def move_right(self):
        self.x += 1
    
    # Move the piece one square down
    def move_down(self):
        self.y += 1
    
    # Rotate the piece
    def rotate(self):
        self.shape = list(map(list, zip(*reversed(self.shape))))
    
    # Draw the piece at the (x,y) coordinate (top left corner of the piece)
    def draw_piece(self, screen, x, y):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        colors[self.color],
                        (((self.x + j)* cellSize + x) ,
                         ((self.y + i)* cellSize + y),
                         cellSize,
                         cellSize,),
                    )
                    pygame.draw.rect(
                        screen, 
                        colors["black"], 
                        (((self.x + j)* cellSize + x), 
                        ((self.y + i)* cellSize + y), 
                        cellSize, 
                        cellSize), 
                        1
                    )
                    