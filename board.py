import pygame
from constants import gridHeight, gridWidth, colors, cellSize


class Board:
    
    def __init__(self):
        self.grid = [[0] * gridWidth for _ in range(gridHeight)]
        self.backgroud_color = "black"
        self.color = [[self.backgroud_color] * gridWidth for _ in range(gridHeight)]

    # Test if the movement of the piece is correct
    def is_valid_move(self, shape, newX, newY):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if (shape[i][j] == 1) and (
                    (newY + i >= gridHeight)
                    or (newX + j < 0 or newX + j >= gridWidth)
                    or (self.grid[newY + i][newX + j]==1)
                ):
                    return False
        return True
    
    # Place the piece in the board
    def place_piece(self, piece):
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[0])):
                if piece.shape[i][j] == 1:
                    self.grid[piece.y + i][piece.x + j] = 1
                    self.color[piece.y + i][piece.x + j] = piece.color

    # Check and clear the complete line and return the number of line clear
    def clear_lines(self):
        full_lines = []
        for i in range(gridHeight):
            if all(self.grid[i]):
                full_lines.append(i)
        for line in full_lines:
            self.color.pop(line)
            self.color.insert(0, [self.backgroud_color] * gridWidth)
            self.grid.pop(line)
            self.grid.insert(0, [0] * gridWidth)
        return len(full_lines)
    
    # Return the distance of the max drop position
    def max_drop_position(self,piece):
        i=1
        while self.is_valid_move(piece.shape, piece.x, piece.y+i):
            i+=1
        return i-1
    
    # Draw the board at the (x,y) coordinate (top left corner of the board)
    def draw_board(self, screen, x, y):
        for i in range(gridHeight):
            for j in range(gridWidth):
                pygame.draw.rect(
                    screen,
                    colors[self.color[i][j]],
                    (
                        (j * cellSize) + x,
                        (i * cellSize) + y,
                        cellSize,
                        cellSize,
                    ),
                )
                pygame.draw.rect(
                    screen,
                    colors["black"],
                    (
                        (j * cellSize) + x,
                        (i * cellSize) + y,
                        cellSize,
                        cellSize,
                    ),
                    1,
                )
    # Reset the board 
    def reset(self):
        self.grid = [[0] * gridWidth for _ in range(gridHeight)]
        self.color = [[self.backgroud_color] * gridWidth for _ in range(gridHeight)]
