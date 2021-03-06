import pygame, os, configparser

from scr.config.config import colours
from scr.config.config import levels

from scr.states.state import State
from scr.tilemaps.levels import Level_1, Level_2, Level_3

from scr.states.cutscenes import Cutscene_1, Cutscene_2

from scr.utility.easying import easeOutBack

class Game_world(State):
    """The main menu"""
    def __init__(self, game, first_time = True):
        """Initialize the menu class."""
        super().__init__(game, first_time)

        # JSON
        # 0 -> json_data init the level
        # 1 -> dict with all dialogs for the level

        self.check_cutscenes()

        if self.game.current_level in [1, 2]:
            self.current_level = Level_1(self.game,
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_tiles.png")),
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_entities.png")),
                                         levels[self.game.current_level][0], levels[self.game.current_level][1], self.game.current_level
                                         )

        if self.game.current_level in [3, 4]:
            self.current_level = Level_3(self.game,
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_tiles.png")),
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_entities.png")),
                                         levels[self.game.current_level][0], levels[self.game.current_level][1], self.game.current_level
                                         )

        if self.game.current_level in [5, 6]:
            self.current_level = Level_2(self.game,
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_tiles.png")),
                                         pygame.image.load(os.path.join(self.game.level_directory, "level_" + str(self.game.current_level), "level_" + str(self.game.current_level) + "_entities.png")),
                                         levels[self.game.current_level][0], levels[self.game.current_level][1], self.game.current_level
                                         )
                        
##        self.levels = {
##            0: Level_1(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_0", "level_0_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_0", "level_0_entities.png")), levels[0][0], levels[0][1], 0
##            ),
##            1: Level_1(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_1", "level_1_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_1", "level_1_entities.png")), levels[1][0], levels[1][1], 1
##            ),
##            2: Level_3(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_2", "level_2_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_2", "level_2_entities.png")), levels[2][0], levels[2][1], 2
##            ),
##            3: Level_3(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_3", "level_3_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_3", "level_3_entities.png")), levels[3][0], levels[3][1], 3
##            ),
##            4: Level_3(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_4", "level_4_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_4", "level_4_entities.png")), levels[4][0], levels[4][1], 4
##            ),
##            5: Level_2(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_5", "level_5_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_5", "level_5_entities.png")), levels[5][0], levels[5][1], 5
##            ),
##            6: Level_2(self.game,
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_6", "level_6_tiles.png")),
##                       pygame.image.load(os.path.join(self.game.level_directory, "level_6", "level_6_entities.png")), levels[6][0], levels[6][1], 6
##            )
##        }

    def check_cutscenes(self):
        if self.game.current_level == 0:
            cutscene_1 = Cutscene_1(self.game, True)
            cutscene_1.enter_state()
        if self.game.current_level == 7:
            cutscene_2 = Cutscene_2(self.game, True)
            cutscene_2.enter_state()
        if self.game.current_level == 8:
            self.game.current_level = 0
            self.game.shut_down()        
        
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

        
        

        

