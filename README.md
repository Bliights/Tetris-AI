# Triste
## Table of Contents
1. [Introduction](#1-introduction)
2. [Creation of Tetris](#2-creation-of-tetris)
   1. [Definition of Constants](#i-definition-of-constants-constantspy)
   2. [Creation of the Piece](#ii-creation-of-the-piece-piecepy)
   3. [Creation of the Board](#iii-creation-of-the-board-boardpy)
   4. [Creation of the Clock](#iv-creation-of-the-clock-clockpy)
   5. [Creation of the Status](#v-creation-of-the-status-statuspy)
   6. [Creation of the Display Element](#vi-creation-of-the-display-element-displaypy)
   7. [Creation of the Game](#vii-creation-of-the-game-tetrisgamepy)
   8. [Execution of the Game](#viii-execution-of-the-game-mainpy)
3. [Creation of the ai](#3-creation-of-the-ai)
4. [Training](#4-training)
   1. [Creating a population](#i-creating-a-population)
   2. [Where the training unfolds](#ii-where-the-training-unfolds)
5. [How to run](#5-how-to-run)
6. [Demo](#6-demo)
7. [Contributors](#7-contributors)

### 1. Introduction
***
This project proposal aims to delve deeply into the game Tetris, focusing on two essential aspects. Firstly, it involves faithfully recreating the game Tetris and conducting an in-depth analysis of its functioning, design, and history. Secondly, this project seeks to develop an Artificial Intelligence (AI) capable of mastering Tetris to the extent of never losing.

The first part of the project entails a meticulous analysis of Tetris, breaking down its mechanics, design principles, and historical evolution. This analysis will shed light on the elements that have contributed to making Tetris an enduring cultural phenomenon and explain its consistent appeal.

The second component of the project is equally fascinating, involving the development of an Artificial Intelligence (AI) system that can achieve exceptional mastery of Tetris, avoiding losses altogether. By creating an AI capable of surpassing human-like strategic thinking and adaptability within the Tetris environment, we aim to push the boundaries of AI capabilities and explore potential applications of this technology in the realms of gaming, problem-solving, and AI research.

### 2. Creation of Tetris
***
Firstly, we recreated Tetris. To achieve this, we decided to use the Pygame library for display and opted for object-oriented programming for all aspects of game management.

#### i. Definition of Constants (constants.py)
***
To kick off this project, we began by defining the game's constants. These include the dimensions of the grid, cell size, frames per second (fps), max score (for saving), the different shapes of the pieces, colors associated with each shape, and all the colors necessary for display.

<details>
<summary>Show Code Preview</summary>

```python
gridWidth = 10
gridHeight = 20
cellSize = 20

fps = 60
maxscore = 2316200


shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]

color_per_shape = [
    "cyan",
    "yellow",
    "red",
    "green",
    "blue",
    "orange",
    "purple",
]

colors = {"black": (0, 0, 0), 
          "white": (255, 255, 255),
          "blue": (0, 0, 255),
          "green": (83, 218, 63),
          "red": (234, 20, 28),
          "yellow": (254, 251, 52),
          "purple": (221, 10, 178),
          "cyan": (1, 237, 250),
          "orange": (255, 200, 46)
          }
```
</details>

#### ii. Creation of the Piece (piece.py)
***
Next, we created the class responsible for the game pieces. To achieve this, we generated a random number using the random library to randomly select a shape from our pre-defined list of shapes (defined in the constants.py file). This allowed us to assign a shape and color to our piece.

We then assigned the initial coordinates for when the pieces are first generated. These initial coordinates include a y-axis coordinate of 0 (considering an inverted y-axis) and an x-coordinate of grid size/2 - piece width/2, which gives us the top-left coordinate of the piece.

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

Then, we created all the movements that our piece can perform, including right, left, down, and rotation.

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

We also created a function that generates a list of strings containing instructions to move a piece to a specific position with a certain number of rotations. This method will be useful later for implementing the AI.

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

Finally, for displaying the piece, we created two methods. One method displays it on a screen at the coordinate x + piece.x, y + piece.y, and the second method displays its shadow on the grid at the same coordinates, except for the y-coordinate where we add the distance to reach the bottom of the grid.

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

#### iii. Creation of the Board (board.py)
***
To create the board, we initialized a list that corresponds to our grid. The value of 0 corresponds to an empty space, and the value of 1 corresponds to a block. We also initialized another grid responsible solely for storing the colors.

<details>
<summary>Show Code Preview</summary>

```python
import pygame
from constants import gridHeight, gridWidth, colors, cellSize
import copy

class Board:
    
    def __init__(self):
        self.grid = [[0] * gridWidth for _ in range(gridHeight)]
        self.backgroud_color = "black"
        self.color = [[self.backgroud_color] * gridWidth for _ in range(gridHeight)]

```
</details>

Next, we created a method to test if moving a shape to a new position was possible. (Note: we didn't use "piece" instead of "shape" for practical reasons related to rotation.)

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

To handle game management, we created several methods:

- One method to permanently place a shape on the board (useful when the shape can no longer move),
- One method to check if there are lines that need to be cleared and, if so, to clear them and return the number of cleared lines,
- One method to obtain the maximum position along the y-axis in its current state.

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

Furthermore, we also created several methods to retrieve important information that will be useful in the creation of the AI:

- One method returning the average height of the columns.
- One method returning the bumpiness (Bumpiness generally corresponds to the difference in height between adjacent columns on the board).
- One method returning the number of holes in the grid structure.
- One method returning the number of blocks in the rightmost column (column used for Tetris, cleared with the line).
- One method returning the maximum height of the grid.
- One method returning the number of open holes that only a bar can fill.

<details>
<summary>Show Code Preview</summary>

```python
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

    # Get the max height of the highest line
    def get_maximum_line_height(self):
        maxHeight=0
        for i in range(gridHeight):
            for j in range(gridWidth):
                if(self.grid[i][j] == 1 and maxHeight==0):
                    maxHeight=gridHeight-i
        return maxHeight

    # Get the number of open holes that are bigger than 3 (only a bar can fill up the hole)    
    def get_number_open_holes(self):
        numberOpenHoles=0
        peaks=[0]*gridWidth
        for i in range(gridWidth):
            j=0
            while j<gridHeight and self.grid[j][i]==0:        
                j+=1
            peaks[i]=gridHeight-j
        for i in range(gridWidth):
            if(i==0):
                if peaks[i+1]-peaks[i]>3:
                    numberOpenHoles+=(peaks[i+1]-peaks[i])//4
            elif(i==gridWidth-1):
                if peaks[i-1]-peaks[i]>3:
                    numberOpenHoles+=(peaks[i-1]-peaks[i])//4
            else:
                if min(peaks[i-1],peaks[i+1])-peaks[i]>3:
                    numberOpenHoles+=(min(peaks[i-1],peaks[i+1])-peaks[i])//4
        return numberOpenHoles
```
</details>

We also created a method allowing us to obtain, for a shape, all the future positions it can have in the grid (T-spins are not included, nor are slow drops to move the shape at the last moment).

<details>
<summary>Show Code Preview</summary>

```python
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
```
</details>

Finally, we created a method to display the board at coordinates (x, y) with coordinates at the top left of the board. Additionally, we created a method to completely reset all elements of this class.

<details>
<summary>Show Code Preview</summary>

```python
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

```
</details>

#### iv. Creation of the Clock (clock.py)
***
The clock that we used is the clock integrated into the Pygame library, and our class allows limiting the execution to a certain number of FPS using the tick function.

<details>
<summary>Show Code Preview</summary>

```python
import pygame
from constants import fps

class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = fps  

    def tick(self):
        return self.clock.tick(self.fps)
```
</details>

#### v. Creation of the Status (status.py)
***
The Status class is used to define the game status and manage the movement of the pieces. This function allows for easy modification and better organization.

<details>
<summary>Show Code Preview</summary>

```python
class Status:
    # Initialyse the game status
    def __init__(self):
        self.game_status = "Home"
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False
        self.drop = False
        self.rotate_limiter = True
        self.drop_limiter = True
    
    def set_game_over(self):
        self.game_status = "Game over"
    
    def set_home(self):
        self.game_status = "Home"
    
    def set_solo(self):
        self.game_status = "Solo"
    
    def set_ai(self):
        self.game_status = "AI"
    
    def is_home(self):
        return self.game_status == "Home"
        
    def is_game_over(self):
        return self.game_status == "Game over"
    
    def is_solo(self):
        return self.game_status == "Solo" 
    
    def is_ai(self):
        return self.game_status == "AI"
    
    # Reset only the control
    def reset_controls(self):
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False
        self.drop = False
        self.rotate_limiter = True
        self.drop_limiter = True
    
    def reset(self):
        self.game_status = "Home"
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False
        self.drop = False
        self.rotate_limiter = True
        self.drop_limiter = True
```
</details>

#### vi. Creation of the Display Element (display.py)
***
This class allows creating display elements on a screen created by the Pygame library. With it, you can create buttons or simply textual display. Buttons are very useful as they allow clear management of mouse movement detection by the user, and with the `mouse_in_element` function, it's easy to determine if the user has clicked on the button.

<details>
<summary>Show Code Preview</summary>

```python
import pygame
from constants import colors

class Display_Element:
    
    def __init__(self,
                 x,
                 y,
                 text,
                 policeSize,
                 textColor,
                 buttonLength = 0,
                 buttonHeight = 0,
                 buttonInsideColor = "",
                 buttonBorderColor = ""):
        self.x = x
        self.y = y
        self.text = text
        self.policeSize = policeSize
        self.textColor = textColor
        self.buttonLength = buttonLength
        self.buttonHeight = buttonHeight
        self.buttonInsideColor = buttonInsideColor
        self.buttonBorderColor = buttonBorderColor
    
    def mouse_in_element(self):
        if self.buttonLength!=0 and self.buttonHeight!=0:
            mouse = pygame.mouse.get_pos()
            if self.x - self.buttonLength//2 <= mouse[0] <= self.x + self.buttonLength//2:
                if self.y - self.buttonHeight//2 <= mouse[1] <= self.y + self.buttonHeight//2:
                    return True
        else:
            return False
    
    def draw(self,screen):
        if self.buttonLength!=0 and self.buttonHeight!=0:
            pygame.draw.rect(screen,
                         colors[self.buttonInsideColor],
                         (self.x-self.buttonLength//2,
                          self.y-self.buttonHeight//2,
                          self.buttonLength,
                          self.buttonHeight)
                         )
        
            pygame.draw.rect(screen,
                         colors[self.buttonBorderColor],
                         (self.x-self.buttonLength//2,
                          self.y-self.buttonHeight//2,
                          self.buttonLength,
                          self.buttonHeight),
                         1
                         )
        
        police = pygame.font.Font(None, self.policeSize)
        text_to_draw = police.render(self.text, True, colors[self.textColor])
        text_rect = text_to_draw.get_rect(center=(self.x,self.y))
        screen.blit(text_to_draw, text_rect)
```
</details>

#### vii. Creation of the Game (tetrisgame.py)
***
The initialization of a game instance includes the current piece, the next piece, the board, the clock, the level, the score, the total number of cleared lines, the gravity speed, the gravity timer, the status, and various display elements.

<details>
<summary>Show Code Preview</summary>

```python
from constants import gridWidth, gridHeight, cellSize, maxscore
from board import Board
from clock import Clock
from piece import Piece
from status import Status
from display import Display_Element


class TetrisGame:
    def __init__(self,screen):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.clock = Clock()
        self.score = 0
        self.level = 0
        self.totaLinesClear = 0
        self.gravity_speed = 48
        self.gravity_timer = 0
        self.status = Status()
        self.display_elements = {
            "Home_menuText" : Display_Element(screen.get_width()//2,
                                              screen.get_height()//10,
                                              "Menu",
                                              100,
                                              "black"
                                              ),
            "Home_soloButton" : Display_Element(screen.get_width()//2,
                                                screen.get_height()//10 + screen.get_height()//10,
                                                "solo mode",
                                                30,
                                                "black",
                                                100,
                                                50,
                                                "cyan",
                                                "black"
                                                ),
            "Home_aiButton" : Display_Element(screen.get_width()//2,
                                              screen.get_height()//10+2*screen.get_height()//10,
                                              "AI mode",
                                              30,
                                              "black",
                                              100,
                                              50,
                                              "yellow",
                                              "black"
                                              ),
            "Home_exitButton" : Display_Element(screen.get_width()//2,
                                                screen.get_height()//10+3*screen.get_height()//10,
                                                "Exit",
                                                30,
                                                "black",
                                                100,
                                                50,
                                                "red",
                                                "black"
                                                ),
            "Solo_scoreText" : Display_Element(screen.get_width()//2,
                                                (screen.get_height()- gridHeight*cellSize)//2- 20,
                                                "Score : "+str(self.score),
                                                30,
                                                "black"
                                                ),
            "Solo_levelText" : Display_Element(screen.get_width()//2,
                                                (screen.get_height()- gridHeight*cellSize)//2- 40,
                                                "Level : "+str(self.level),
                                                30,
                                                "black"
                                                ),
            "Solo_exitButton" : Display_Element(screen.get_width()-70,
                                                40,
                                                "Exit",
                                                30,
                                                "black",
                                                100,
                                                50,
                                                "red",
                                                "black"
                                                ),
            "Solo_homeButton" : Display_Element(screen.get_width()-70,
                                                100,
                                                "Menu",
                                                30,
                                                "black",
                                                100,
                                                50,
                                                "green",
                                                "black"
                                                ),
            "Game_over_gameOverText" : Display_Element(screen.get_width()//2,
                                                       screen.get_height()//2,
                                                       "Game Over",
                                                       100,
                                                       "red"
                                                       ),
            "Game_over_scoreText" : Display_Element(screen.get_width()//2,
                                                    screen.get_height()//2-screen.get_height()//8,
                                                    "Your score : "+ str(self.score),
                                                    50,
                                                    "white"
                                                    ),
            "Game_over_maxScoreText" : Display_Element(screen.get_width()//2,
                                                    screen.get_height()//2-2*screen.get_height()//8,
                                                    "Best score : "+ str(maxscore),
                                                    50,
                                                    "white"
                                                    ),
            "Game_over_resetButton" : Display_Element(screen.get_width()//2,
                                                    screen.get_height()//2+screen.get_height()//10,
                                                    "Restart",
                                                    30,
                                                    "white",
                                                    100,
                                                    50,
                                                    "black",
                                                    "white"
                                                    ),
            "Game_over_homeButton" : Display_Element(screen.get_width()//2,
                                                    screen.get_height()//2+2*screen.get_height()//10,
                                                    "Menu",
                                                    30,
                                                    "white",
                                                    100,
                                                    50,
                                                    "black",
                                                    "white"
                                                    ),
            "Game_over_exitButton" : Display_Element(screen.get_width()//2,
                                                    screen.get_height()//2+3*screen.get_height()//10,
                                                    "Exit",
                                                    30,
                                                    "white",
                                                    100,
                                                    50,
                                                    "black",
                                                    "white"
                                                    ),
            }
```
</details>

Then, we created all the necessary functions for the movement of the pieces while checking that the movements were allowed. We also defined a function to determine if the game is over.

<details>
<summary>Show Code Preview</summary>

```python
    def move_piece_left(self):
        if self.board.is_valid_move(self.current_piece.shape, 
                                    self.current_piece.x - 1 , 
                                    self.current_piece.y):
            self.current_piece.move_left()
            return True
        else:
            return False
    
    def move_piece_right(self):
        if self.board.is_valid_move(self.current_piece.shape, 
                                    self.current_piece.x + 1, 
                                    self.current_piece.y):
            self.current_piece.move_right()
            return True
        else:
            return False
    
    def check_game_over(self):
        if self.current_piece.y == 0 and (
        not self.board.is_valid_move(
        self.current_piece.shape, 
        self.current_piece.x, 
        self.current_piece.y)):
            self.status.set_game_over()
            self.update_score_max()
            self.display_elements["Game_over_scoreText"].text = "Your score : "+ str(self.score)
    
    def move_piece_down(self):
        if self.board.is_valid_move(self.current_piece.shape, 
                                    self.current_piece.x, 
                                    self.current_piece.y + 1):
            
            self.current_piece.move_down()
            return True
        else:
            if not self.status.is_game_over():
                self.board.place_piece(self.current_piece)
                self.gravity_timer = 0
                lineClear = self.board.clear_lines()
                self.totaLinesClear += lineClear
                self.update_score(lineClear)
                
                self.current_piece = self.next_piece
                self.next_piece = Piece()
            
                self.check_game_over()
                return False
        
    def rotate_piece(self):
         rotated_piece = list(map(list, zip(*reversed(self.current_piece.shape))))
         if self.board.is_valid_move(rotated_piece, 
                                     self.current_piece.x, 
                                     self.current_piece.y):
             self.current_piece.rotate()
             return True
         else:
             return False

    def drop(self):
        is_drop=False
        while self.move_piece_down():
            is_drop=True
        return is_drop
```
</details>

Next, we created functions responsible for gravity, level, score, and modification of the maximum score in the constants file.

<details>
<summary>Show Code Preview</summary>

```python
    def update_gravity(self):
        self.gravity_timer += 1
        if self.gravity_timer == self.gravity_speed:
            self.move_piece_down()
            self.gravity_timer = 0

    def update_level(self):
        if self.totaLinesClear<=10:
            self.level = 1
            self.gravity_speed = 43
        elif self.totaLinesClear<=20:
            self.level = 2
            self.gravity_speed = 38
        elif self.totaLinesClear<=30:
            self.level = 3
            self.gravity_speed = 33
        elif self.totaLinesClear<=40:
            self.level = 4
            self.gravity_speed = 28
        elif self.totaLinesClear<=50:
            self.level = 5
            self.gravity_speed = 23
        elif self.totaLinesClear<=60:
            self.level = 6
            self.gravity_speed = 18
        elif self.totaLinesClear<=70:
            self.level = 7
            self.gravity_speed = 13
        elif self.totaLinesClear<=80:
            self.level = 8
            self.gravity_speed = 8
        elif self.totaLinesClear<=90:
            self.level = 9
            self.gravity_speed = 6
        elif self.totaLinesClear<=100:
            self.level = 10
            self.gravity_speed = 5
        elif self.totaLinesClear<=110:
            self.level = 11
            self.gravity_speed = 4
        elif self.totaLinesClear<=120:
            self.level = 12
            self.gravity_speed = 3
        elif self.totaLinesClear<=130:
            self.level = 13
            self.gravity_speed = 2
        elif self.totaLinesClear<=140:
            self.level = 14
            self.gravity_speed = 1
            
    def update_score(self, lineClear):
        score_multiplier = {1: 40, 2: 100, 3: 300, 4: 1200}
        if lineClear in score_multiplier:
            toAdd = score_multiplier[lineClear]
            self.score += toAdd * (self.level + 1)
            self.display_elements["Solo_scoreText"].text = "Score : "+str(self.score)
            self.update_level()
            self.display_elements["Solo_levelText"].text = "Level : "+str(self.level)
             
    def update_score_max(self):
        if self.score>maxscore:
            with open('constants.py', 'r') as file:
                lines = file.readlines()

            for i in range(len(lines)):
                if 'maxscore' in lines[i]:
                    lines[i] = 'maxscore = ' + str(self.score) +"\n"

            with open('constants.py', 'w') as file:
                file.writelines(lines)
```
</details>

Finally, we defined all the necessary functions to display the different menus and to reset the game.

<details>
<summary>Show Code Preview</summary>

```python
    def draw_home_menu(self,screen):
        self.display_elements["Home_menuText"].draw(screen)
        self.display_elements["Home_soloButton"].draw(screen)
        self.display_elements["Home_aiButton"].draw(screen)
        self.display_elements["Home_exitButton"].draw(screen)       
        
    def draw_solo_game(self, screen):  
        self.board.draw_board(screen,
                              (screen.get_width() - gridWidth * cellSize) // 2, 
                              (screen.get_height() - gridHeight * cellSize) // 2)
        self.current_piece.draw_shadow(screen,
                                       (screen.get_width() - gridWidth* cellSize)//2,
                                       (screen.get_height() - gridHeight* cellSize)//2,
                                       self.board.max_drop_position(self.current_piece))
        self.current_piece.draw_piece(screen,
                                      (screen.get_width() - gridWidth* cellSize)//2,
                                      (screen.get_height() - gridHeight* cellSize)//2)
        self.next_piece.draw_piece(screen,
                                   (screen.get_width() + 3*gridWidth* cellSize//5)//2,
                                   (screen.get_height() - 3*gridHeight* cellSize//9)//2)
        self.display_elements["Solo_scoreText"].draw(screen)
        self.display_elements["Solo_levelText"].draw(screen)
        self.display_elements["Solo_exitButton"].draw(screen)
        self.display_elements["Solo_homeButton"].draw(screen)
            
    def draw_game_over(self,screen):
        self.display_elements["Game_over_gameOverText"].draw(screen)
        self.display_elements["Game_over_scoreText"].draw(screen)
        self.display_elements["Game_over_maxScoreText"].draw(screen)
        self.display_elements["Game_over_resetButton"].draw(screen)
        self.display_elements["Game_over_homeButton"].draw(screen)
        self.display_elements["Game_over_exitButton"].draw(screen)
               
    def reset(self):
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 0
        self.totaLinesClear = 0
        self.gravity_timer = 0
        self.gravity_speed = 48
        self.status.reset()
        self.display_elements["Solo_scoreText"].text = str(self.score)
        self.display_elements["Game_over_scoreText"].text = str(self.score)
     
```
</details>

#### viii. Execution of the Game (main.py)
***
To run the game, we initialized a game window and the game itself. Then, we looped through actions to be performed based on different statuses within a while loop.

<details>
<summary>Show Code Preview</summary>

```python
import pygame
from constants import colors
from tetrisgame import TetrisGame
from ai import Ai

pygame.init()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")
display.fill(colors["white"]) 
game = TetrisGame(display) 
ai = Ai(display)
ai.fixMultiplier()
game.clock.tick()
running = True

while running:
    if game.status.is_home():
        display.fill(colors["white"])
        game.draw_home_menu(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                # solo mode
                if game.display_elements["Home_soloButton"].mouse_in_element():
                    game.reset()
                    game.status.set_solo()
                # AI mode
                elif game.display_elements["Home_aiButton"].mouse_in_element():
                    game.reset()
                    game.status.set_ai()
                # Exit button
                elif game.display_elements["Home_exitButton"].mouse_in_element():
                    running = False
                    
    elif game.status.is_solo():
        display.fill(colors["white"])
        game.draw_solo_game(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.status.move_left = True
                elif event.key == pygame.K_RIGHT:
                    game.status.move_right = True
                elif event.key == pygame.K_DOWN:
                    game.status.move_down = True
                elif event.key == pygame.K_UP:
                    game.status.rotate = True
                elif event.key == pygame.K_SPACE:
                    game.status.drop = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.status.move_left = False
                elif event.key == pygame.K_RIGHT:
                    game.status.move_right = False
                elif event.key == pygame.K_DOWN:
                    game.status.move_down = False
                elif event.key == pygame.K_UP:
                    game.status.rotate = False
                    game.status.rotate_limiter = True
                elif event.key == pygame.K_SPACE:
                    game.status.drop = False
                    game.status.drop_limiter = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Menu button
                if game.display_elements["Solo_homeButton"].mouse_in_element():
                    game.reset()
                    game.status.set_home()
                # Exit button
                elif game.display_elements["Solo_exitButton"].mouse_in_element():
                    running = False
            
        if game.status.move_left:
            game.move_piece_left()
        elif game.status.move_right:
            game.move_piece_right()
        elif game.status.move_down:
            game.move_piece_down()
        elif game.status.rotate and game.status.rotate_limiter:
            game.rotate_piece()
            game.status.rotate_limiter = False
        elif game.status.drop and game.status.drop_limiter:
            game.drop()
            game.status.drop_limiter = False
        
        pygame.time.delay(30)
        game.update_gravity()
        game.clock.tick()
    
    elif game.status.is_game_over():   
        display.fill(colors["black"])
        game.status.reset_controls()
        game.draw_game_over(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Restart button
                if game.display_elements["Game_over_resetButton"].mouse_in_element():
                    game.reset()
                    game.status.set_solo()
                # Menu button
                elif game.display_elements["Game_over_homeButton"].mouse_in_element():
                    game.reset()
                    game.status.set_home()
                # Exit button
                elif game.display_elements["Game_over_exitButton"].mouse_in_element():
                    running = False
                    
    elif game.status.is_ai():
        if ai.game.status.is_solo():
            display.fill(colors["white"])
            ai.game.draw_solo_game(display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Menu button
                    if game.display_elements["Solo_homeButton"].mouse_in_element():
                        ai.reset()
                        game.status.set_home()
                    # Exit button
                    elif game.display_elements["Solo_exitButton"].mouse_in_element():
                        running = False
            if(len(ai.movementPlan)==0):
                ai.addMoves(ai.getBestMove())
            ai.nextMove()
            pygame.time.delay(30)
            ai.game.update_gravity()
            ai.game.clock.tick()
            
        elif ai.game.status.is_game_over():
            display.fill(colors["black"])
            ai.game.draw_game_over(display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart button
                    if ai.game.display_elements["Game_over_resetButton"].mouse_in_element():
                        ai.reset()
                    # Menu button
                    elif ai.game.display_elements["Game_over_homeButton"].mouse_in_element():
                        ai.reset()
                        game.status.set_home()
                    # Exit button
                    elif ai.game.display_elements["Game_over_exitButton"].mouse_in_element():
                        running = False
        
    pygame.display.update()

pygame.quit()
```
</details>

### 3. Creation of the AI
***
To develop an AI that plays Tetris, we opted to create a function responsible for estimating the cost of each potential move. To achieve this, we selected various parameters that we deemed relevant for our AI. These parameters include the number of holes, bumpiness, the number of lines cleared by the move, the number of blocks in the rightmost column, the average peak, the number of open holes and the maximum line height. Once these parameters were defined, we created a method that randomly selects a number between 0 and 100 for each multiplier.
Furthermore, we equipped our AI with its own Tetris game instance and a list to store all its future movements.

<details>
<summary>Show Code Preview</summary>

```python
from tetrisgame import TetrisGame
from random import random, uniform, randint
import copy

class Ai:
    def __init__(self, screen):
        self.game = TetrisGame(screen)
        self.game.status.set_solo()
        self.multipliers = {}
        self.fitness = 0
        self.movementPlan = []
        self.screen = screen

    def fixMultiplier(self):      
        self.multipliers = {
            'holeCountMultiplier': 99.19118639408582, 
            'bumpinessMultiplier': 27.7875228027838133, 
            'lineClearMultiplier': 40.255678920084427, 
            'blocksRightLaneMultiplier': 30.57724385974105, 
            'averagePeakMultiplier': 13.22146800503185, 
            'maximumLineHeightMultiplier': 24.76785274467504, 
            'openHoleCountMultiplier': 29.540934405234474
        }
        
    def randomizeMultipliers(self):
        self.multipliers = {
            "holeCountMultiplier": uniform(0, 100),
            "bumpinessMultiplier": uniform(0, 100),
            "lineClearMultiplier": uniform(0, 100),
            "blocksRightLaneMultiplier": uniform(0, 100),
            "averagePeakMultiplier": uniform(0, 100),
            "maximumLineHeightMultiplier": uniform(0, 100),
            "openHoleCountMultiplier": uniform(0, 100)
        }
```
</details>

We then created a function to calculate the player's fitness, enabling us to compare different players based on their game results. Following that, we developed a function to execute the next move and remove it from the list of pending moves. Additionally, we designed a function to place a piece on a board at a specific position.

<details>
<summary>Show Code Preview</summary>

```python
    def calculateFitness(self):
        if self.game.totaLinesClear != 0:
            self.fitness = self.game.score / self.game.totaLinesClear
        else:
            self.fitness = 0

    def nextMove(self):
        if self.movementPlan[0] == "right":
            self.game.move_piece_right()
        elif self.movementPlan[0] == "left":
            self.game.move_piece_left()
        elif self.movementPlan[0] == "rotate":
            self.game.rotate_piece()
        else:
            self.game.drop()
        self.movementPlan.pop(0)

    def placePieceInBoardAtPosition(self, board, piece, position):
        piece.x = position[0]
        piece.y = position[1]
        for i in range(position[2]):
            piece.rotate()
        if board.is_valid_move(piece.shape, piece.x, piece.y):
            board.place_piece(piece)
```
</details>

To further the process, we defined the method that calculates the cost of a move for a certain piece on a given board. With this function, we were able to create the function that determines the best move. The latter generates all possible combinations of boards based on the active piece and the next piece. It calculates the cost of each move to determine the best possible combination.With this, we can determine where the current piece should go, and we repeat the process for the next piece.

<details>
<summary>Show Code Preview</summary>

```python
    def costOfMove(self, board, piece, position):
        boardCopy = copy.deepcopy(board)
        pieceCopy = copy.deepcopy(piece)

        self.placePieceInBoardAtPosition(boardCopy, pieceCopy, position)

        lineClear = boardCopy.clear_lines()
        holes = boardCopy.get_number_holes()
        bumpiness = boardCopy.get_bumpiness()
        blocksRightmostLane = boardCopy.count_blocks_in_rightmost_lane()
        averagePeaks = boardCopy.get_average_peaks()
        maximumLineHeight = boardCopy.get_maximum_line_height()
        openHoles = boardCopy.get_number_open_holes()

        costLineClear = 0
        if lineClear != 4:
            costLineClear = self.multipliers["lineClearMultiplier"] * lineClear
        else:
            costLineClear = -self.multipliers["lineClearMultiplier"] * lineClear

        return (
            self.multipliers["holeCountMultiplier"] * holes
            + self.multipliers["bumpinessMultiplier"] * bumpiness
            + costLineClear
            + self.multipliers["blocksRightLaneMultiplier"] * blocksRightmostLane
            + self.multipliers["averagePeakMultiplier"] * averagePeaks
            + self.multipliers["maximumLineHeightMultiplier"] * maximumLineHeight
            +self.multipliers["openHoleCountMultiplier"] * openHoles
        )

    def getBestMove(self):
        positionsCurrent = self.game.board.get_all_position(self.game.current_piece)
        costPositions = []
        BestPositionsNext = []
        for i in range(len(positionsCurrent)):
            costPositions.append(
                self.costOfMove(
                    self.game.board, self.game.current_piece, positionsCurrent[i]
                )
            )

            boardCopy = copy.deepcopy(self.game.board)
            pieceCopy = copy.deepcopy(self.game.current_piece)
            self.placePieceInBoardAtPosition(boardCopy, pieceCopy, positionsCurrent[i])

            positionsNext = boardCopy.get_all_position(self.game.next_piece)
            costNext = []
            for j in range(len(positionsNext)):
                costNext.append(
                    self.costOfMove(boardCopy, self.game.next_piece, positionsNext[j])
                )

            indexBestNextMove = costNext.index(min(costNext))
            BestPositionsNext.append(positionsNext[indexBestNextMove])
            costPositions[i] += costNext[indexBestNextMove]

        indexBestMoves = costPositions.index(min(costPositions))
        return self.game.current_piece.get_path_to_position(
            positionsCurrent[indexBestMoves]
        )
```
</details>

Finally, we created a method for adding a move to the list of pending moves, along with a method to make our AI move (useful during training) and to clone or reset it.

<details>
<summary>Show Code Preview</summary>

```python
    def addMoves(self, path):
        for i in range(len(path)):
            self.movementPlan.append(path[i])

    def mutate(self, mutationRate):
        if random() < mutationRate:
            num = randint(0, len(self.multipliers)-1)
            count=0
            for key, value in self.multipliers.items():
                if num == count:
                    self.multipliers[key] = uniform(0, 100)
                    break
                count+=1

    def clone(self):
        clone = Ai(self.screen)
        clone.multipliers = self.multipliers
        return clone

    def reset(self):
        self.game.reset()
        self.game.status.set_solo()
        self.fitness = 0
        self.movementPlan = []
```
</details>

### 4. Training 
***
#### i. Creating a Population
***
To create a population, we need several parameters, including its size, the maximum number of generations, the mutation chances, the percentage of the best to retain, and the chance to retain poor AIs. Each population comprises a list of AIs.

<details>
<summary>Show Code Preview</summary>

```python
from ai import Ai
from random import random,choice,getrandbits

class Population:
    def __init__(self,
                 populationSize,
                 maxGeneration,
                 chanceToMutate,
                 gradedRetainPercent,
                 chanceRetainNongraded,
                 screen
                 ):
        
        self.populationSize = populationSize
        self.aiPopulation = []
        for i in range(self.populationSize):
            newAi=Ai(screen)
            newAi.randomizeMultipliers()
            newAi.game.status.set_solo()
            self.aiPopulation.append(newAi)
        
        self.maxGeneration = maxGeneration
        self.generation = 0;
        self.chanceToMutate = chanceToMutate
        self.gradedRetainPercent = gradedRetainPercent 
        self.chanceRetainNongraded = chanceRetainNongraded 
        
        self.gradedIndividualCount = (int)(self.populationSize*self.gradedRetainPercent)
        
        self.bestAi = Ai(screen)
        self.maxlineClear = 0
```
</details>

Next, we created the functions necessary for training: updating the AI, calculating the overall fitness for all AIs, sorting the population based on fitness, and selecting the best AI in the generation.

<details>
<summary>Show Code Preview</summary>

```python
    def update(self,i):
        while self.aiPopulation[i].game.status.is_solo() and self.aiPopulation[i].game.totaLinesClear<10000:
            if(len(self.aiPopulation[i].movementPlan)==0):
                self.aiPopulation[i].addMoves(self.aiPopulation[i].getBestMove())
            self.aiPopulation[i].nextMove()
            self.aiPopulation[i].game.update_gravity()
        print(i)
            
    def calculateAiFitnesses(self): 
        for i in range(self.populationSize): 
            self.aiPopulation[i].calculateFitness()
    
    def populationSortedByFitness(self):
        self.aiPopulation = sorted(self.aiPopulation, key=lambda x: x.fitness, reverse=True)
          
    def setBestAi(self):
        self.bestAi = self.aiPopulation[0];
        for i in range(self.populationSize): 
            if (self.aiPopulation[i].fitness>self.bestAi.fitness):
                self.bestAi=self.aiPopulation[i]
```
</details>

To conclude the training, we defined the method for keeping the AIs (the parents) and creating offspring to complete the population. Additionally, we also created the methods to potentially mutate the population and the function responsible for the entire natural selection process.

<details>
<summary>Show Code Preview</summary>

```python
    def createParents(self):
        parents = self.aiPopulation[:self.gradedIndividualCount]
        for individual in self.aiPopulation[self.gradedIndividualCount:]:
            if random() < self.chanceRetainNongraded:
                parents.append(individual)
        self.aiPopulation = parents
        for i in range(len(self.aiPopulation)):
            self.aiPopulation[i].reset()
        return parents
    
    def populationMutation(self):
        for i in range(len(self.aiPopulation)):
            self.aiPopulation[i].mutate(self.chanceToMutate)
        
    def createChildren(self,father,mother):
        children = father.clone()
        children.reset()
        for key, value in father.multipliers.items():
            children.multipliers[key]=father.multipliers[key] if getrandbits(1) else mother.multipliers[key]
        return children
            
    def naturalSelection(self):
        self.calculateAiFitnesses()
        self.populationSortedByFitness()
        self.setBestAi()
        self.maxlineClear=self.bestAi.game.totaLinesClear
        
        self.createParents()
        self.populationMutation()
        
        childrenNumber = self.populationSize - len(self.aiPopulation)
        children = []
        while len(children) < childrenNumber:
            father = choice(self.aiPopulation)
            mother = choice(self.aiPopulation)
            if father!=mother:
                children.append(self.createChildren(father,mother))
        
        self.aiPopulation.extend(children)
        self.generation+=1
```
</details>

#### ii. Where the Training Unfolds
***
This is where the training takes place. If you also want to train the AI, you simply need to execute the `training.py` file and wait until the AI that meets your criteria is found. This training involves simultaneously running all AIs using multithreading (it's not true parallelism, but it allows for updating almost all AIs at the same time, saving a considerable amount of time). We chose not to use multiprocessing, as it proved less efficient than multithreading in our tests. Multiprocessing allowed only 16 games to be executed simultaneously on our computers, resulting in longer waiting times for a large population.

Following these game rounds, natural selection occurs. This process continues until the AI meets the criteria we defined (clear line count criteria to prevent the AI from playing indefinitely).

<details>
<summary>Show Code Preview</summary>

```python
from population import Population
import pygame
import concurrent.futures
import time


start_time = time.time()
pygame.init()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")

populationSize = 100
maxGeneration = 10000
chanceToMutate = 0.1
gradedRetainPercent = 0.2
chanceRetainNongraded = 0.05
population = Population(populationSize,maxGeneration,chanceToMutate,gradedRetainPercent,chanceRetainNongraded,display)

while population.generation<population.maxGeneration and population.maxlineClear<10000:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(population.update,range(len(population.aiPopulation))) 
    population.naturalSelection()
    print(f'Max Lines clear : {population.maxlineClear} ({population.generation} generation)')
    print(population.bestAi.multipliers)
    
print(f"Solution found at generation n {population.generation}")
print(population.bestAi.multipliers)

pygame.quit()

end_time = time.time()
execution_time = end_time - start_time
print(f"Temps d'exécution : {execution_time/60} minutes")
```
</details>

### 5. How to run
***
1. Install a python distribution on your computer
   [python.org](https://www.python.org/)

2. Install all the necessary library
   `pip install -r requirements.txt`

3. Run the main file to play the game
   `python main.py`

### 6. Demo
***
YouTube link : [Triste](https://youtu.be/8CYik-HB55k)

### 7. Contributors
***
|            Name            |      College      |    Department    |                   Email                   |
| :------------------------: | :---------------: | :--------------: | :---------------------------------------: |
|    MOLLY-MITTON Clément    |    Engineering    | Computer Science |       clement.mollymitton@gmail.com       |
|  BENDAVID OUYOUSSEF Sarah  |    Engineering    | Computer Science |        sarahbendavid@dartybox.com         |
|        HUBNER James        | Arts and Sciences | Criminal Justice |               jhub@uab.edu                |
| ARROUET LE BRIGNONEN Aubin |    Engineering    | Computer Science | aubin.arrouet_le_brignonen@edu.devinci.fr |
|        MOBLEY Erin         |    Engineering    | Computer Science |      erin.mobley@email.saintleo.edu       |
