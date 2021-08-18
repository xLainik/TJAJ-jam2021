import pygame, os
from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State

from scr.utility.easying import easeOutBack

class Options_menu(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game

        self.timer = 0
        
        self.load_sprites()
        
    def load_sprites(self):
        self.options_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 22, "OPTIONS", colours["white"], False, self.game.SCREEN_WIDTH//2, 30, True)
        self.scale_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 22, "-    SCALE    +", colours["white"], False, self.game.SCREEN_WIDTH, 106, False)

        self.scale_down_button = pygame.Rect(-100,100,60,32)
        self.scale_up_button = pygame.Rect(-100,100,60,32)
        self.back_to_menu_button = pygame.Rect(-250,160,150,32)

        self.back_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 22, "BACK", colours["white"], False, self.game.SCREEN_WIDTH, 180, True)
        
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

        mx, my = pygame.mouse.get_pos()
        mx, my = int(mx/self.game.SCALE), int(my/self.game.SCALE)

        if self.scale_up_button.collidepoint(mx, my) and self.game.click:
            self.game.SCALE += 1
            self.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
            self.timer = 0
        if self.scale_down_button.collidepoint(mx, my) and self.game.click:
            self.game.SCALE -= 1
            self.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
            self.timer = 0
        if self.back_to_menu_button.collidepoint(mx,my) and self.game.click:
            self.exit_state(restart = True)

        if self.timer < 60:
            self.timer += 1
            self.scale_down_button.x = int(easeOutBack(self.timer, -86, (89 + (self.game.GAME_WIDTH-210)//2), 60, s=1))
            self.scale_up_button.x = self.scale_down_button.x + 156
            
            self.back_to_menu_button.x = int(easeOutBack(self.timer, -250, (250 + (self.game.GAME_WIDTH-150)//2), 60, s=1))
        
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])

        self.options_txt.update(self.game.game_canvas)    
        self.scale_txt.update(self.game.game_canvas, x = self.scale_down_button.x + 28)
        self.back_txt.update(self.game.game_canvas, x = self.back_to_menu_button.x + 78)
        
        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.scale_up_button, width = 4)
        pygame.draw.rect(self.game.game_canvas, colours["red"], self.scale_down_button, width = 4)
        pygame.draw.rect(self.game.game_canvas, colours["white"], self.back_to_menu_button, width = 4)
        

        

