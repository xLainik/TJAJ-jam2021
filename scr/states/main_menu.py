import pygame, os

from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State
from scr.states.options_menu import Options_menu

from scr.states.game_world import Game_world

from scr.utility.easying import easeOutBack

from scr.utility.resize_image import resize

class Main_menu(State):
    """The main menu"""
    def __init__(self, game, first_time = True):
        """Initialize the menu class."""
        super().__init__(game, first_time)
        
        self.load_sprites()

        self.hover = False

        self.timer = 0

        self.game.load_sfx("menu_hover.wav", "menu_click.wav")

        self.game.all_sfx["menu_hover"].set_volume(0.5 * self.game.sfx_global_volume/100)
        self.game.all_sfx["menu_click"].set_volume(0.5 * self.game.sfx_global_volume/100)

    def load_sprites(self):

        self.bg_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "fondo 2.png")), self.game.SCALE, 4)
        self.start_button = pygame.Rect(450 * self.game.SCALE,94 * self.game.SCALE,150 * self.game.SCALE,32 * self.game.SCALE)
        self.options_button = pygame.Rect(-250 * self.game.SCALE,154 * self.game.SCALE,150 * self.game.SCALE,32 * self.game.SCALE)

        self.inactive_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton apagado.png")), self.game.SCALE, 4)
        self.active_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton activo.png")), self.game.SCALE, 4)

        self.start_button_img = self.inactive_button_img
        self.options_button_img = self.inactive_button_img

        self.start_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 16, "JUGAR", colours["white"], True, (self.game.GAME_WIDTH * self.game.SCALE), 110 * self.game.SCALE, True, self.game.SCALE)
        self.options_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 16, "OPCIONES", colours["white"], True, (self.game.GAME_WIDTH * self.game.SCALE), 170 * self.game.SCALE, True, self.game.SCALE)
    
    def update(self):
        """Update the menu state."""

        mx, my = pygame.mouse.get_pos()

        if self.start_button.collidepoint(mx, my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.start_button_img = self.active_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.high_res_canvas.fill((0,0,0))
                game_world = Game_world(self.game, True)
                game_world.enter_state()
                game_world.check_cutscenes()
        elif self.options_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.options_button_img = self.active_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.high_res_canvas.fill((0,0,0))
                options = Options_menu(self.game, True)
                options.enter_state()
        else:
            self.hover = False
            self.start_button_img = self.inactive_button_img
            self.options_button_img = self.inactive_button_img
        

        if self.timer < 60:
            self.timer += 1
            self.start_button.x = int((self.game.GAME_WIDTH * self.game.SCALE) - self.options_button.width - (easeOutBack(self.timer, -100, (100 + (self.game.GAME_WIDTH-150)//2), 60, s=1) * self.game.SCALE))
            self.options_button.x = int((self.game.GAME_WIDTH * self.game.SCALE) - self.options_button.width - (easeOutBack(self.timer, -250, (250 + (self.game.GAME_WIDTH-150)//2), 60, s=1) * self.game.SCALE))
        
    def render(self):
        """Render the menu state."""

        self.game.high_res_canvas.blit(self.bg_img, (0,0))
        
        self.game.high_res_canvas.blit(self.start_button_img, ((self.start_button.x-10), self.start_button.y))
        self.game.high_res_canvas.blit(self.options_button_img, ((self.options_button.x-10), self.options_button.y))

        self.start_txt.update(self.game.high_res_canvas, x = self.start_button.x + 80 * self.game.SCALE, scale = self.game.SCALE)
        self.options_txt.update(self.game.high_res_canvas, x = self.options_button.x + 79 * self.game.SCALE, scale = self.game.SCALE)        
