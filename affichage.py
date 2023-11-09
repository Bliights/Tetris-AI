import pygame
from constants import colors

def draw_button(screen,
                x,
                y,
                buttonLength,
                buttonHeight,
                text,
                policeSize,
                textColor,
                buttonInsideColor,
                buttonBorderColor):
    pygame.draw.rect(screen,
                     colors[buttonInsideColor],
                     (x-buttonLength//2,
                      y-buttonHeight//2,
                      buttonLength,
                      buttonHeight)
                     )
    
    pygame.draw.rect(screen,
                     colors[buttonBorderColor],
                     (x-buttonLength//2,
                      y-buttonHeight//2,
                      buttonLength,
                      buttonHeight),
                     1
                     )
    
    police = pygame.font.Font(None, policeSize)
    text_to_draw = police.render(text, True, colors[textColor])
    text_rect = text_to_draw.get_rect(center=(x,y))
    screen.blit(text_to_draw, text_rect)


def mouse_in_button(buttonX,buttonY,buttonLength,buttonHeight):
    mouse = pygame.mouse.get_pos()
    if buttonX-buttonLength//2<=mouse[0]<=buttonX+buttonLength//2:
        if buttonY-buttonHeight//2<=mouse[1]<=buttonY+buttonHeight//2:
            return True
        else:
            return False
        
def draw_text(screen,
                x,
                y,
                text,
                policeSize,
                textColor
                ):
    police = pygame.font.Font(None, policeSize)
    text_to_draw = police.render(text, True, colors[textColor])
    text_rect = text_to_draw.get_rect(center=(x,y))
    screen.blit(text_to_draw, text_rect)
