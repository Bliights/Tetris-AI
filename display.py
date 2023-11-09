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

