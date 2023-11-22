import pygame
from constants import gridHeight, gridWidth, colors, cellSize
import copy

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
    
    # Get the pick on the board
    def get_average_peaks(self):
        peaks=[0]*gridWidth
        for i in range(gridWidth):
            j=0
            while j<gridHeight and self.grid[j][i]==0:        
                j+=1
            peaks[i]=gridHeight-j
        return sum(peaks)/gridWidth
    
    # Get the bumpiness of the board
    def get_bumpiness(self):
        previousHeight=0
        bumpiness = 0
        for i in range(gridWidth):
            j=0
            while j<gridHeight and self.grid[j][i]==0:
                j+=1
            if i>0:
                bumpiness+=abs(previousHeight+j-gridHeight)
            previousHeight=gridHeight-j
        return bumpiness
    
    # Get the the number of holes in the struct
    def get_number_holes(self):
        blockFound = False
        holes_count = 0
        for i in range(gridWidth):
            for j in range(gridHeight):
                if(self.grid[j][i] == 1):
                    blockFound = True
                elif(self.grid[j][i] == 0 and blockFound == True):
                    holes_count+=1   
            blockFound = False
        return holes_count
    
    # Count the number of block in the rightmost lane
    def count_blocks_in_rightmost_lane(self):
        blocks_right_lane = 0
        for j in range(gridHeight):
            if (self.grid[j][gridWidth-1]==1):
                blocks_right_lane+=1
        return blocks_right_lane
    
    # Get all the position possible for a piece in the board   
    def get_all_position(self,pieceGiven):
        positions = []
        piece = copy.deepcopy(pieceGiven)
        for r in range(4):
            movePossible=True
            if r!=0:
                rotated_piece = list(map(list, zip(*reversed(piece.shape))))
                if self.is_valid_move(rotated_piece, 
                                        piece.x, 
                                        piece.y):
                    piece.rotate()
                else:
                    movePossible=False
            if movePossible:
                for i in range(gridWidth-len(piece.shape[0])+1):
                    movePossible=True
                    horizontal_mvt = i-piece.x
                    for h in range(abs(horizontal_mvt)):
                        if(horizontal_mvt>0):
                            if self.is_valid_move(piece.shape, 
                                                piece.x + h+1, 
                                                piece.y)==False:
                                movePossible=False
                                break
                        else :
                            if self.is_valid_move(piece.shape, 
                                                 piece.x -h-1, 
                                                 piece.y)==False:
                                movePossible=False
                                break
                    if movePossible:
                        j=piece.y
                        while self.is_valid_move(piece.shape,i,j):
                            j+=1
                        positions.append((i,j-1,r))        
        return positions
    
    # Get the max height of the highest line
    def get_maximum_line_height(self):
        maxHeight=0
        for i in range(gridHeight):
            for j in range(gridWidth):
                if(self.grid[i][j] == 1 and maxHeight==0):
                    maxHeight=gridHeight-i
        return maxHeight
    
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

