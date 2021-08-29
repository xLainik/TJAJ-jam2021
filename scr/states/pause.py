import pygame, os

from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State

from scr.utility.easying import easeOutBack

from scr.utility.resize_image import resize

class Pause(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)
        
        self.load_sprites()

        self.hover = False

        self.timer = 0

        self.game.load_sfx("menu_hover.wav", "menu_click.wav")

        self.game.all_sfx["menu_hover"].set_volume(0.5 * self.game.sfx_global_volume/100)
        self.game.all_sfx["menu_click"].set_volume(0.5 * self.game.sfx_global_volume/100)
        

    def load_sprites(self):
        self.resume_button = pygame.Rect(450 * self.game.SCALE,84 * self.game.SCALE,150 * self.game.SCALE,32 * self.game.SCALE)

        self.inactive_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton apagado.png")), self.game.SCALE, 4)
        self.active_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton activo.png")), self.game.SCALE, 4)

        self.resume_button_img = self.inactive_button_img

        self.resume_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 16, "SEGUIR", colours["white"], True, (self.game.GAME_WIDTH * self.game.SCALE), 100 * self.game.SCALE, True, self.game.SCALE)
    
    def update(self):
        """Update the menu state."""

        mx, my = pygame.mouse.get_pos()

        if self.resume_button.collidepoint(mx, my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.resume_button_img = self.active_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.high_res_canvas.fill((0,0,0))
                self.exit_state(False)
        else:
            self.hover = False
            self.resume_button_img = self.inactive_button_img

        if self.timer < 60:
            self.timer += 1
            self.resume_button.x = int((self.game.GAME_WIDTH * self.game.SCALE) - self.resume_button.width - (easeOutBack(self.timer, -100, (100 + (self.game.GAME_WIDTH-150)//2), 60, s=1) * self.game.SCALE))
            
    def render(self):
        """Render the pause state."""
        self.game.high_res_canvas.fill(colours["black"])

        self.game.high_res_canvas.blit(self.resume_button_img, ((self.resume_button.x-10), self.resume_button.y))

        self.resume_txt.update(self.game.high_res_canvas, x = self.resume_button.x + 80 * self.game.SCALE, scale = self.game.SCALE)      
