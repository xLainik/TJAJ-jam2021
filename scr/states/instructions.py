import pygame, os
from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State

class Instructions(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game

        self.load_sprites()
        
    def load_sprites(self):
        self.instructions_txt = Text(self.game.game_canvas, os.path.join(self.game.font_directory,"FreePixel.ttf"), 18, "Instructions", colours["white"], False, 8, 72, False)
  
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])

        self.instructions_txt.update(self.game.game_canvas)    

        

        

