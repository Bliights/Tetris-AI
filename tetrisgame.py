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
                 