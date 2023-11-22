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
ai.game.status.set_solo()
game.clock.tick()
running = True

while running:
    if game.status.is_home():
        display.fill(colors["white"])
        game.draw_home_menu(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                pygame.quit()
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
                    pygame.quit()
                    
    elif game.status.is_ai():
        if ai.game.status.is_solo():
            display.fill(colors["white"])
            ai.game.draw_solo_game(display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if(len(ai.movementPlan)==0):
                ai.addMoves(ai.getBestMove())
            ai.nextMove()
            pygame.time.delay(30)
            ai.game.update_gravity()
            ai.game.clock.tick()
            
        elif ai.game.status.is_game_over():
            display.fill(colors["black"])
            game.status.reset_controls()
            game.draw_game_over(display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart button
                    if game.display_elements["Game_over_resetButton"].mouse_in_element():
                        ai.game.reset()
                        ai.game.status.set_solo()
                    # Menu button
                    elif game.display_elements["Game_over_homeButton"].mouse_in_element():
                        ai.game.reset()
                        ai.game.status.set_solo()
                        game.status.set_home()
                    # Exit button
                    elif game.display_elements["Game_over_exitButton"].mouse_in_element():
                        pygame.quit()
        
    pygame.display.update()