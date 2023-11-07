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
    
    def draw_button(self,screen,x,y,buttonLength,buttonHeight,text,policeSize,
                    textColor,buttonColor):
        pygame.draw.rect(screen,buttonColor,(x-buttonLength//2,y-buttonHeight//2,buttonLength,buttonHeight),1)
        police = pygame.font.Font(None, policeSize)
        textToDraw = police.render(text, True, textColor)
        text_rect = textToDraw.get_rect(center=(x,y))
        screen.blit(textToDraw, text_rect)
    
    def draw_score(self,screen):
        police = pygame.font.Font(None, 36)
        text = police.render("Score: " + str(self.score), True, colors["black"])
        screen.blit(text, (10, 10))
        
        
    def draw_game_over(self,screen):
        police = pygame.font.Font(None, 100)
        text = police.render("Game Over", True, colors["red"])
        text_rect = text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        screen.blit(text, text_rect)
        
        # Score display
        police = pygame.font.Font(None, 50)
        text = police.render("Your score : "+ str(self.score), True, colors["white"])
        text_rect = text.get_rect(center=(screen.get_width()//2,screen.get_height()//2-screen.get_height()//8))
        screen.blit(text, text_rect)
        # Reset Button
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//2+screen.get_height()//10,
                         100,
                         50,
                         "Restart",
                         30,
                         colors["white"],
                         colors["white"])
        # Menu
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//2+2*screen.get_height()//10,
                         100,
                         50,
                         "Menu",
                         30,
                         colors["white"],
                         colors["white"])
        # Exit button
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//2+3*screen.get_height()//10,
                         100,
                         50,
                         "Exit",
                         30,
                         colors["white"],
                         colors["white"])
    
    def draw_menu(self,screen):
        police = pygame.font.Font(None, 100)
        text = police.render("Menu", True, colors["black"])
        text_rect = text.get_rect(center=(screen.get_width()//2,screen.get_height()//10))
        screen.blit(text, text_rect)
        
        # solo mode Button
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//10+screen.get_height()//10,
                         100,
                         50,
                         "solo mode",
                         30,
                         colors["black"],
                         colors["black"])
        # Ai mode button
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//10+2*screen.get_height()//10,
                         100,
                         50,
                         "AI mode",
                         30,
                         colors["black"],
                         colors["black"])
        # Exit button
        self.draw_button(screen,
                         screen.get_width()//2,
                         screen.get_height()//10+3*screen.get_height()//10,
                         100,
                         50,
                         "Exit",
                         30,
                         colors["black"],
                         colors["black"])
        
    def mouse_in_button(self,mouseX,mouseY,buttonX,buttonY,buttonLength,buttonHeight):
        if buttonX-buttonLength//2<=mouseX<=buttonX+buttonLength//2:
            if buttonY-buttonHeight//2<=mouseY<=buttonY+buttonHeight//2:
                return True
        else:
            return False
        
    def draw_game(self, screen):  
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
                self.current_piece = game.next_piece
                self.next_piece = Piece()
                self.check_game_over()
       
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
    
    def reset(self):
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.clock.reset()
        self.score = 0
        self.level = 0
        self.gravity_timer = gravity
        self.game_over = False
    

pygame.init()
game = TetrisGame() 

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
running = True
mode="menu"

while running:
    if mode=="menu":
        display.fill(colors["white"])
        game.draw_menu(display)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # solo mode
                if game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//10+screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    mode="solo"
                # AI mode
                elif game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//10+2*screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    mode="AI"
                # Exit button
                elif game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//10+3*screenHeight//10,
                                   100,
                                   50):
                    pygame.quit()
                    
    elif mode == "solo":
        rotate_limit=True
        while not game.game_over:
            display.fill(colors["white"])
            game.draw_game(display)
            pygame.display.update()
            game.clock.tick()
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
                        rotate_limit=True
            
            if key_state[pygame.K_LEFT]:
                game.board.move_piece_left(game.current_piece)
            elif key_state[pygame.K_RIGHT]:
                game.board.move_piece_right(game.current_piece)
            elif key_state[pygame.K_DOWN]:
                game.board.move_piece_down(game.current_piece)
            elif key_state[pygame.K_UP] and rotate_limit:
                game.board.rotate_piece(game.current_piece)
                rotate_limit=False
            
            game.clock.tick()  
            
            game.update()
        
        
        display.fill(colors["black"])
        key_state = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_DOWN: False,
            pygame.K_UP: False
        }
        game.draw_game_over(display)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Restart button
                if game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//2+screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                # Menu button
                elif game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//2+2*screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    mode="menu"
                # Exit button
                elif game.mouse_in_button(mouse[0],
                                   mouse[1],
                                   screenWidth//2,
                                   screenHeight//2+3*screenHeight//10,
                                   100,
                                   50):
                    pygame.quit()
                    
    elif mode == "AI":
        temp=0
        
    pygame.display.update()
