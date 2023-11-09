from constants import fps, gravity, gridWidth, gridHeight, cellSize, maxscore
from board import Board
from clock import Clock
from piece import Piece
from status import Status
from affichage import draw_button, draw_text


class TetrisGame:
    def __init__(self):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.clock = Clock()
        self.score = 0
        self.level = 0
        self.gravity_timer = gravity
        self.status = Status()
    
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
    
    def move_piece_down(self):
        if self.board.is_valid_move(self.current_piece.shape, 
                                    self.current_piece.x, 
                                    self.current_piece.y + 1):
            
            self.current_piece.move_down()
            return True
        else:
            if not self.status.is_game_over():
                self.board.place_piece(self.current_piece)
            
                lineClear = self.board.clear_lines()
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
    
    def update_gravity(self):
        self.gravity_timer -= 1
        if self.gravity_timer == 0:
            self.move_piece_down()
            self.gravity_timer = gravity
            
                
    def update_score(self, lineClear):
        score_multiplier = {1: 40, 2: 100, 3: 300, 4: 1200}
        if lineClear in score_multiplier:
            toAdd = score_multiplier[lineClear]
            self.score += toAdd * (self.level + 1)
    
    def update_score_max(self):
        if self.score>maxscore:
            with open('constants.py', 'r') as file:
                lines = file.readlines()

            for i in range(len(lines)):
                if 'maxscore' in lines[i]:
                    lines[i] = 'maxscore = ' + str(self.score)

            with open('constants.py', 'w') as file:
                file.writelines(lines)
    
    def draw_home_menu(self,screen):
        draw_text(screen,
                  screen.get_width()//2,
                  screen.get_height()//10,
                  "Menu",
                  100,
                  "black"
                  )
        # Solo mode Button
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//10+screen.get_height()//10,
                    100,
                    50,
                    "solo mode",
                    30,
                    "black",
                    "cyan",
                    "black")
    
        # Ai mode butto
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//10+2*screen.get_height()//10,
                    100,
                    50,
                    "AI mode",
                    30,
                    "black",
                    "yellow",
                    "black")
        # Exit button
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//10+3*screen.get_height()//10,
                    100,
                    50,
                    "Exit",
                    30,
                    "black",
                    "red",
                    "black")
        
    def draw_solo_game(self, screen):  
        self.board.draw_board(screen,
                              (screen.get_width() - gridWidth * cellSize) // 2, 
                              (screen.get_height() - gridHeight * cellSize) // 2)
        
        self.current_piece.draw_piece(screen,
                                      (screen.get_width() - gridWidth* cellSize)//2,
                                      (screen.get_height() - gridHeight* cellSize)//2)
        
        self.next_piece.draw_piece(screen,
                                      (screen.get_width() + 3*gridWidth* cellSize//5)//2,
                                      (screen.get_height() - 3*gridHeight* cellSize//9)//2)
        draw_text(screen,
                  screen.get_width()//2,
                  (screen.get_height()- gridHeight*cellSize)//2- 20,
                  str(self.score),
                  35,
                  "black"
                  )
        
    def draw_game_over(self,screen):
        draw_text(screen,
                  screen.get_width()//2,
                  screen.get_height()//2,
                  "Game Over",
                  100,
                  "red"
                  )
        # Score display
        draw_text(screen,
                  screen.get_width()//2,
                  screen.get_height()//2-screen.get_height()//8,
                  "Your score : "+ str(self.score),
                  50,
                  "white"
                  )
        # Reset Button
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//2+screen.get_height()//10,
                    100,
                    50,
                    "Restart",
                    30,
                    "white",
                    "black",
                    "white")
        # Menu
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//2+2*screen.get_height()//10,
                    100,
                    50,
                    "Menu",
                    30,
                    "white",
                    "black",
                    "white")
        # Exit button
        draw_button(screen,
                    screen.get_width()//2,
                    screen.get_height()//2+3*screen.get_height()//10,
                    100,
                    50,
                    "Exit",
                    30,
                    "white",
                    "black",
                    "white")
               
    def reset(self):
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 0
        self.gravity_timer = fps
        self.status.reset()
                 