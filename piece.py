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
    
    # Get the instruction to get the piece to a specific position
    def get_path_to_position(self,position):
        horizontal_mvt = position[0]-self.x
        rotations = position[2]
        path=[]
        for i in range(rotations):
            path.append("rotate")
        for i in range(abs(horizontal_mvt)):
            if horizontal_mvt>0:
                path.append("right")
            else:
                path.append("left")
        path.append("drop")
        return path
    
    # Draw the piece at the (x+piece.x,y+piece.y) coordinate (top left corner of the piece)
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
    
    # Draw the shadow of the piece at the (x+piece.x,y+piece.y+drop) coordinate
    def draw_shadow(self, screen, x, y,drop):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        colors["black"],
                        (((self.x + j)* cellSize + x) ,
                         ((self.y + drop + i)* cellSize + y),
                         cellSize,
                         cellSize,),
                    )
                    pygame.draw.rect(
                        screen, 
                        colors[self.color], 
                        (((self.x + j)* cellSize + x), 
                        ((self.y + drop + i)* cellSize + y), 
                        cellSize, 
                        cellSize), 
                        1
                    )
                    