from constants import fps, gridWidth, gridHeight, cellSize, maxscore
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
        self.gravity_speed = int(fps*(1-0.1*self.level))
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
                                                str(self.score),
                                                35,
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
        self.gravity_timer += 1
        if self.gravity_timer == self.gravity_speed:
            self.move_piece_down()
            self.gravity_timer = 0

    def update_level(self):
        if self.score == 2400:
            self.level = 2
        elif self.score == 5000:
            self.level = 3
        elif self.score == 10000:
            self.level = 4
        elif self.score == 20000:
            self.level = 5
        elif self.score == 30000:
            self.level = 6
        elif self.score == 40000:
            self.level = 7
        elif self.score == 50000:
            self.level = 8
        elif self.score == 80000:
            self.level = 9
        self.gravity_speed = int(fps*(1-0.1*self.level))
            
    def update_score(self, lineClear):
        score_multiplier = {1: 40, 2: 100, 3: 300, 4: 1200}
        if lineClear in score_multiplier:
            toAdd = score_multiplier[lineClear]
            self.score += toAdd * (self.level + 1)
            self.display_elements["Solo_scoreText"].text = str(self.score)
            self.update_level()
             
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
        self.display_elements["Home_menuText"].draw(screen)
        self.display_elements["Home_soloButton"].draw(screen)
        self.display_elements["Home_aiButton"].draw(screen)
        self.display_elements["Home_exitButton"].draw(screen)       
        
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
        self.display_elements["Solo_scoreText"].draw(screen)
        
    def draw_game_over(self,screen):
        self.display_elements["Game_over_gameOverText"].draw(screen)
        self.display_elements["Game_over_scoreText"].draw(screen)
        self.display_elements["Game_over_resetButton"].draw(screen)
        self.display_elements["Game_over_homeButton"].draw(screen)
        self.display_elements["Game_over_exitButton"].draw(screen)
               
    def reset(self):
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 0
        self.gravity_timer = 0
        self.gravity_speed = int(fps*(1-0.1*self.level))
        self.status.reset()
        self.display_elements["Solo_scoreText"].text = str(self.score)
        self.display_elements["Game_over_scoreText"].text = str(self.score)
                 