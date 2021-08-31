import pygame, os

from scr.config.config import levels

from scr.states.state import State

from scr.dialog import Dialog

from scr.utility.resize_image import resize

class Cutscene_1(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game

        img_sequence = []
        for img in os.listdir(os.path.join(self.game.image_directory, "image sequences", "cine inicio")):
            timer = int(img.split("_")[-1].split("_")[-1].split(".")[0])
            img_sequence.append([timer, resize(pygame.image.load(os.path.join("scr", "assets", "images", "image sequences", "cine inicio", img)), self.game.SCALE, 3.4)])

        self.dialog = Dialog(game, levels[1][1]["dialog_5"], "dialog_5", 1, "dialog_5_images.json", False, img_sequence)

    def update(self):
        """Update the menu state."""
        self.dialog.update()

        # Empezar juego
        self.game.current_level = 1
        self.exit_state()
            
    def render(self):
        """Render the menu state."""
        pass

        
class Cutscene_2(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game

        img_sequence = []
        for img in os.listdir(os.path.join(self.game.image_directory, "image sequences", "cine final unico")):
            timer = int(img.split("_")[-1].split("_")[-1].split(".")[0])
            img_sequence.append([timer, resize(pygame.image.load(os.path.join("scr", "assets", "images", "image sequences", "cine final unico", img)), self.game.SCALE, 3.4)])

        self.dialog = Dialog(game, levels[1][1]["dialog_6"], "dialog_6", 1, "dialog_6_images.json", False, img_sequence)

    def update(self):
        """Update the menu state."""
        self.dialog.update()

        # Reiniciar juego y cerrar:
        self.game.current_level = 0
        self.game.restart()       
            
    def render(self):
        """Render the menu state."""
        pass  

        

