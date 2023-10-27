import pygame
from constants import gridHeight, gridWidth, colors, cellSize

class Board:
    def __init__(self):
        self.grid = [[0] * gridWidth for _ in range(gridHeight)]
        self.color = [["black"] * gridWidth for _ in range(gridHeight)]
       
        
    def is_valid_move(self,shape,newX,newY):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if (shape[i][j] == 1) and (
                    ( newX + i >= gridHeight)
                    or ( newY + j < 0 or newY + j >= gridWidth)
                    or (self.grid[newX + i][newY + j])
                ):
                    return False
        return True    


    def move_piece_left(self, piece):
        if self.is_valid_move(piece.shape,piece.x,piece.y - 1):
            piece.y -= 1
            return True
        else:
            return False


    def move_piece_right(self, piece):
        if self.is_valid_move(piece.shape,piece.x,piece.y + 1):
            piece.y += 1
            return True
        else:
            return False


    def move_piece_down(self, piece):
        if self.is_valid_move(piece.shape,piece.x + 1,piece.y):
            piece.x += 1
            return True
        else:
            return False


    def rotate_piece(self, piece):
        rotated_shape = list(map(list, zip(*reversed(piece.shape))))
        if self.is_valid_move(rotated_shape,piece.x,piece.y):
            piece.shape = rotated_shape
            return True
        else:
            return False


    def place_piece(self,piece):
        if self.is_valid_move(
            piece.shape,
            piece.x,
            piece.y,
        ):
            for i in range(len(piece.shape)):
                for j in range(len(piece.shape[0])):
                    if piece.shape[i][j] == 1:
                        self.grid[piece.x + i][piece.y + j] = 1
                        self.color[piece.x + i][piece.y + j] = piece.colorName
        
            
    def clear_lines(self):
        full_lines = []
        for i in range(gridHeight):
            if all(self.grid[i]):
                full_lines.append(i)
        for line in full_lines:
            self.color.pop(line)
            self.color.insert(0, ["black"] * gridWidth)
            self.grid.pop(line)
            self.grid.insert(0, [0] * gridWidth)
        return len(full_lines)


    def draw_board(self,screen):
       for i in range(gridHeight):
        for j in range(gridWidth):
            pygame.draw.rect(
                screen, 
                colors[self.color[i][j]], 
                (j * cellSize, 
                 i * cellSize, 
                 cellSize, 
                 cellSize)
            )
            pygame.draw.rect(
                screen, 
                colors["black"], 
                (j * cellSize, 
                i * cellSize, 
                cellSize, 
                cellSize), 
                1
            )
              
            
    def reset(self):
        self.grid = [[0] * gridWidth for _ in range(gridHeight)]
        self.color = [["white"] * gridWidth for _ in range(gridHeight)]