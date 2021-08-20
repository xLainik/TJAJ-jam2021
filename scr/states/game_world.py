import pygame, os

from scr.config.config import colours
from scr.config.config import levels

from scr.states.state import State
from scr.tilemaps.levels import Level_0

from scr.utility.easying import easeOutBack

class Game_world(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.levels = {
            0: Level_0(self.game,
                     pygame.image.load(os.path.join(self.game.level_directory, "level_0", "level_0_tiles.png")), levels[0]
            )
        }
        self.change_level(self.levels[0])
        
        
    def change_level(self, new_level):
        self.current_level = new_level

    def update(self):
        """Update the menu state."""
        self.current_level.update()
            
    def render(self):
        """Render the menu state."""
        self.current_level.render()

        
        

        
