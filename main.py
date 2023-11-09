import pygame
from constants import colors
from tetrisgame import TetrisGame
from affichage import mouse_in_button

pygame.init()
game = TetrisGame() 
game.clock.tick()

# Initialize game display
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h

display = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Tetris")
display.fill(colors["white"]) 
running = True
rotate_limit=True

while running:
    if game.status.is_home():
        display.fill(colors["white"])
        game.draw_home_menu(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # solo mode
                if mouse_in_button(screenWidth//2,
                                   screenHeight//10+screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    game.status.set_solo()
                # AI mode
                elif mouse_in_button(screenWidth//2,
                                   screenHeight//10+2*screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    game.status.set_ai()
                # Exit button
                elif mouse_in_button(screenWidth//2,
                                   screenHeight//10+3*screenHeight//10,
                                   100,
                                   50):
                    pygame.quit()
                    
    elif game.status.is_solo():
        display.fill(colors["white"])
        game.draw_solo_game(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.status.move_left = True
                elif event.key == pygame.K_RIGHT:
                    game.status.move_right = True
                elif event.key == pygame.K_DOWN:
                    game.status.move_down = True
                elif event.key == pygame.K_UP:
                    game.status.rotate = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    game.status.move_left = False
                elif event.key == pygame.K_RIGHT:
                    game.status.move_right = False
                elif event.key == pygame.K_DOWN:
                    game.status.move_down = False
                elif event.key == pygame.K_UP:
                    game.status.rotate = False
                    rotate_limit=True
            
        if game.status.move_left:
            game.move_piece_left()
        elif game.status.move_right:
            game.move_piece_right()
        elif game.status.move_down:
            game.move_piece_down()
        elif game.status.rotate and rotate_limit:
            game.rotate_piece()
            rotate_limit=False
        
        game.clock.tick()   
        game.update_gravity()
        game.clock.tick()
    
    elif game.status.is_game_over():   
        display.fill(colors["black"])
        game.status.reset_controls()
        game.draw_game_over(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Restart button
                if mouse_in_button(screenWidth//2,
                                   screenHeight//2+screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    game.status.set_solo()
                # Menu button
                elif mouse_in_button(screenWidth//2,
                                   screenHeight//2+2*screenHeight//10,
                                   100,
                                   50):
                    game.reset()
                    game.status.set_home()
                # Exit button
                elif mouse_in_button(screenWidth//2,
                                   screenHeight//2+3*screenHeight//10,
                                   100,
                                   50):
                    pygame.quit()
                    
    elif game.status.is_ai():
        temp=0
        
    pygame.display.update()