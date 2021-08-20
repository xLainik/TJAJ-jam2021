import pygame, os

from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State
from scr.states.instructions import Instructions
from scr.states.options_menu import Options_menu

from scr.states.game_world import Game_world

from scr.utility.easying import easeOutBack

class Main_menu(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)
        
        self.load_sprites()

        self.hover = False

        self.timer = 0

        self.game.load_sounds("menu_hover.wav", "menu_click.wav")

        self.game.all_sounds["menu_hover"].set_volume(0.5)
        self.game.all_sounds["menu_click"].set_volume(0.5)

    def load_sprites(self):
        self.start_button = pygame.Rect(450,100,150,32)
        self.options_button = pygame.Rect(-250,160,150,32)
            

        self.start_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 22, "START", colours["white"], False, self.game.GAME_WIDTH//2, 120, True)
        self.options_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 22, "OPTIONS", colours["white"], False, self.game.GAME_WIDTH//2, 180, True)
    
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

        mx, my = pygame.mouse.get_pos()
        mx, my = int(mx/self.game.SCALE), int(my/self.game.SCALE)

        if self.start_button.collidepoint(mx, my):
            if not(self.hover):
                self.game.all_sounds["menu_hover"].play()
                self.hover = True
            if self.game.click:
                self.game.all_sounds["menu_click"].play()
                game_world = Game_world(self.game)
                game_world.enter_state()
        elif self.options_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sounds["menu_hover"].play()
                self.hover = True
            if self.game.click:
                self.game.all_sounds["menu_click"].play()
                options = Options_menu(self.game)
                options.enter_state()
        else: self.hover = False
        

        if self.timer < 60:
            self.timer += 1
            self.start_button.x = int(self.game.GAME_WIDTH - self.options_button.width - easeOutBack(self.timer, -100, (100 + (self.game.GAME_WIDTH-150)//2), 60, s=1))
            self.options_button.x = int(self.game.GAME_WIDTH - self.options_button.width - easeOutBack(self.timer, -250, (250 + (self.game.GAME_WIDTH-150)//2), 60, s=1))
        
  
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])

        pygame.draw.rect(self.game.game_canvas, colours["white"], self.start_button, width=4)
        pygame.draw.rect(self.game.game_canvas, colours["white"], self.options_button, width=4)

        self.start_txt.update(self.game.game_canvas, x = self.start_button.x + 76)
        self.options_txt.update(self.game.game_canvas, x = self.options_button.x + 75)

        