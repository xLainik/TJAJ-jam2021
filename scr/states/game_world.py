import pygame, os, configparser

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

        # JSON
        # 0 -> json_data init the level
        # 1 -> dict with all dialogs for the level

        self.levels = {
            0: Level_0(self.game,
                       pygame.image.load(os.path.join(self.game.level_directory, "level_0", "level_0_tiles.png")),
                       pygame.image.load(os.path.join(self.game.level_directory, "level_0", "level_0_entities.png")), levels[0][0], levels[0][1]
            )
        }
        
        self.change_level(self.levels[self.game.current_level])
        
        
    def change_level(self, new_level):
        self.current_level = new_level

    def restart_level(self):
        self.__init__(self.game)

    def update(self):
        """Update the menu state."""
        self.current_level.update()
            
    def render(self):
        """Render the menu state."""
        self.current_level.render()

        
        

        

