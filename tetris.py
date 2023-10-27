import pygame
from constants import gravity, colors
from board import Board
from clock import Clock
from piece import Piece

class TetrisGame:
    def __init__(self):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.clock = Clock()
        self.score = 0
        self.level = 0
        self.gravity_timer = gravity
        self.game_over = False
    
    def draw_score(self,screen):
        police = pygame.font.Font(None, 36)
        text = police.render("Score: " + str(self.score), True, colors["black"])
        screen.blit(text, (10, 10))
    
    def draw_game_over(self,screen):
        police = pygame.font.Font(None, 36)
        text = police.render("Game Over", True, colors["red"])
        screen.blit(text, (screen.get_width()//2, screen.get_height()//2))
    
    def draw(self, screen):  
        self.board.draw_board(screen)
        self.current_piece.draw_piece(screen)
        self.draw_score(screen)
        self.next_piece.draw_next_piece(screen)
    
    def piece_down(self):
        if not self.board.move_piece_down(self.current_piece):
            if not self.check_game_over():
                self.board.place_piece(self.current_piece)
                lineClear = self.board.clear_lines()
                self.add_score(lineClear)
                game.current_piece = game.next_piece
                game.next_piece = Piece()
       
    def update(self):
        if not self.game_over:
            self.gravity_timer -= 1
            if self.gravity_timer == 0:
                self.piece_down()
                self.gravity_timer = gravity
                      
    def check_game_over(self):
        if self.current_piece.x == 0 and (
        not self.board.is_valid_move(
        self.current_piece.shape, 
        self.current_piece.x, 
        self.current_piece.y)):
            self.game_over = True
           
    def add_score(self, lineClear):
        score_multiplier = {1: 40, 2: 100, 3: 300, 4: 1200}
        if lineClear in score_multiplier:
            toAdd = score_multiplier[lineClear]
            self.score += toAdd * (self.level + 1)

    
pygame.init()

game = TetrisGame() 
game.clock.reset()

key_state = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_DOWN: False,
    pygame.K_UP: False
}
# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")
display.fill(colors["white"]) 


#TO DO : create a running variable instead of game over and give the choice to play again
 
while not game.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key_state[pygame.K_LEFT] = True
            elif event.key == pygame.K_RIGHT:
                key_state[pygame.K_RIGHT] = True
            elif event.key == pygame.K_DOWN:
                key_state[pygame.K_DOWN] = True
            elif event.key == pygame.K_UP:
                key_state[pygame.K_UP] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_state[pygame.K_LEFT] = False
            elif event.key == pygame.K_RIGHT:
                key_state[pygame.K_RIGHT] = False
            elif event.key == pygame.K_DOWN:
                key_state[pygame.K_DOWN] = False
            elif event.key == pygame.K_UP:
                key_state[pygame.K_UP] = False
            game.clock.reset_speed()
        
    if key_state[pygame.K_LEFT]:
        game.board.move_piece_left(game.current_piece)
        game.clock.acceleration()
    elif key_state[pygame.K_RIGHT]:
        game.board.move_piece_right(game.current_piece)
        game.clock.acceleration()
    elif key_state[pygame.K_DOWN]:
        game.board.move_piece_down(game.current_piece)
        game.clock.acceleration()
    elif key_state[pygame.K_UP]:
        game.board.rotate_piece(game.current_piece)
        game.clock.acceleration()
        
        
    game.clock.tick()
    
    game.update()
    
    #Draw the board
    display.fill(colors["white"])
    game.draw(display)
    pygame.display.update()
    
    game.clock.tick()




game.draw_game_over(display)


pygame.quit()
