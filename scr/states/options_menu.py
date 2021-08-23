import pygame, os
from scr.config.config import colours
from scr.sprites.text import Text
from scr.states.state import State

from scr.utility.easying import easeOutBack

from scr.utility.resize_image import resize

class Options_menu(State):
    """The main menu"""
    def __init__(self, game):
        """Initialize the menu class."""
        super().__init__(game)

        self.game = game

        self.hover = False

        self.timer = 0
        
        self.load_sprites()

        pygame.mixer.set_num_channels(2)
        
    def load_sprites(self):
        self.options_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 16, "OPCIONES", colours["white"], True, self.game.SCREEN_WIDTH * self.game.SCALE//2, 28 * self.game.SCALE, True, self.game.SCALE)
        self.scale_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, "Tamaño de Pantalla", colours["white"], True, self.game.SCREEN_WIDTH * self.game.SCALE, 75 * self.game.SCALE, False, self.game.SCALE)
        self.sfx_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, "Efectos de Sonido", colours["white"], True, 20 * self.game.SCALE, 115 * self.game.SCALE, False, self.game.SCALE)
        self.music_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, "Musica", colours["white"], True, 88 * self.game.SCALE, 155 * self.game.SCALE, False, self.game.SCALE)

        self.scale_value_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, str(self.game.SCREEN_WIDTH * self.game.SCALE) + "x" + str(self.game.SCREEN_HEIGHT * self.game.SCALE), colours["white"], True, self.game.SCREEN_WIDTH * self.game.SCALE, 80 * self.game.SCALE, True, self.game.SCALE)
        self.sfx_value_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, str(int(self.game.sfx_global_volume)) + "%", colours["white"], True, 20 * self.game.SCALE, 120 * self.game.SCALE, True, self.game.SCALE)
        self.music_value_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 16, str(int(self.game.music_global_volume)) + "%", colours["white"], True, 93 * self.game.SCALE, 160 * self.game.SCALE, True, self.game.SCALE)
        
        self.scale_down_button = pygame.Rect(-100 * self.game.SCALE,66 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)
        self.scale_up_button = pygame.Rect(-100 * self.game.SCALE,66 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)

        self.sfx_down_button = pygame.Rect(-100 * self.game.SCALE,106 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)
        self.sfx_up_button = pygame.Rect(-100 * self.game.SCALE,106 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)

        self.music_down_button = pygame.Rect(-100 * self.game.SCALE,146 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)
        self.music_up_button = pygame.Rect(-100 * self.game.SCALE,146 * self.game.SCALE,24 * self.game.SCALE,26 * self.game.SCALE)
        
        self.back_to_menu_button = pygame.Rect(-250 * self.game.SCALE,202 * self.game.SCALE,150 * self.game.SCALE,32 * self.game.SCALE)
        
        self.inactive_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton apagado.png")), self.game.SCALE, 4)
        self.active_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "boton activo.png")), self.game.SCALE, 4)
        self.inactive_arrow_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "flecha apagada.png")), self.game.SCALE, 4)
        self.active_arrow_button_img = resize(pygame.image.load(os.path.join(self.game.image_directory, "flecha activa.png")), self.game.SCALE, 4)
        
        self.back_to_menu_button_img = self.inactive_button_img

        self.inactive_arrow_right_button_img = self.inactive_arrow_button_img
        self.active_arrow_right_button_img = self.active_arrow_button_img

        self.inactive_arrow_left_button_img = pygame.transform.flip(self.inactive_arrow_right_button_img, True, False).convert_alpha()
        self.active_arrow_left_button_img = pygame.transform.flip(self.active_arrow_right_button_img, True, False).convert_alpha()

        self.scale_arrow_right_button_img = self.inactive_arrow_right_button_img
        self.scale_arrow_left_button_img = self.inactive_arrow_left_button_img
        self.sfx_arrow_right_button_img = self.inactive_arrow_right_button_img
        self.sfx_arrow_left_button_img = self.inactive_arrow_left_button_img
        self.music_arrow_right_button_img = self.inactive_arrow_right_button_img
        self.music_arrow_left_button_img = self.inactive_arrow_left_button_img

        self.back_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 16, "VOLVER", colours["white"], True, self.game.SCREEN_WIDTH * self.game.SCALE, 218 * self.game.SCALE, True, self.game.SCALE)
        
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

        mx, my = pygame.mouse.get_pos()
        mx, my = int(mx * self.game.SCALE/ self.game.RESIZED_SCALE_WIDTH), int(my * self.game.SCALE/ self.game.RESIZED_SCALE_HEIGHT)

        if self.scale_up_button.collidepoint(mx, my) and self.game.SCALE < self.game.MAX_SCALE:
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.scale_arrow_right_button_img = self.active_arrow_right_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.SCALE += 1
                self.game.RESIZED_SCALE_WIDTH, self.game.RESIZED_SCALE_HEIGHT = self.game.screen.get_width()/self.game.SCREEN_WIDTH, self.game.screen.get_height()/self.game.SCREEN_HEIGHT
                self.game.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE), pygame.RESIZABLE)
                self.game.high_res_canvas = pygame.Surface((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas.fill((0,0,0))
                self.game.high_res_canvas.set_colorkey((0,0,0))
                self.__init__(self.game)
        elif self.scale_down_button.collidepoint(mx, my) and self.game.SCALE > 1:
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.scale_arrow_left_button_img = self.active_arrow_left_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.SCALE -= 1
                self.game.RESIZED_SCALE_WIDTH, self.game.RESIZED_SCALE_HEIGHT = self.game.screen.get_width()/self.game.SCREEN_WIDTH, self.game.screen.get_height()/self.game.SCREEN_HEIGHT
                self.game.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE), pygame.RESIZABLE)
                self.game.high_res_canvas = pygame.Surface((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas.fill((0,0,0))
                self.game.high_res_canvas.set_colorkey((0,0,0))
                self.__init__(self.game)
        elif self.sfx_down_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.sfx_arrow_left_button_img = self.active_arrow_left_button_img
            if self.game.click:
                self.game.sfx_global_volume -= 0.8
                if self.game.sfx_global_volume < 0: self.game.sfx_global_volume = 0
                if self.game.click == 1:
                    self.game.all_sfx["menu_click"].play()
        elif self.sfx_up_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.sfx_arrow_right_button_img = self.active_arrow_right_button_img
            if self.game.click:
                self.game.sfx_global_volume += 0.8
                if self.game.sfx_global_volume > 100: self.game.sfx_global_volume = 100
                if self.game.click == 1:
                    self.game.all_sfx["menu_click"].play()
        elif self.music_down_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.music_arrow_left_button_img = self.active_arrow_left_button_img
            if self.game.click:
                self.game.music_global_volume -= 0.8
                if self.game.music_global_volume < 0: self.game.music_global_volume = 0
        elif self.music_up_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.music_arrow_right_button_img = self.active_arrow_right_button_img
            if self.game.click:
                self.game.music_global_volume += 0.8
                if self.game.music_global_volume > 100: self.game.music_global_volume = 100
                
        elif self.back_to_menu_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
                self.back_to_menu_button_img = self.active_button_img
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.game_canvas.fill(colours["black"])
                self.game.state_stack[0].timer = 0
                self.game.state_stack[0].load_sprites()
                self.exit_state()
        else:
            self.hover = False
            self.back_to_menu_button_img = self.inactive_button_img
            self.scale_arrow_right_button_img = self.inactive_arrow_right_button_img
            self.scale_arrow_left_button_img = self.inactive_arrow_left_button_img
            self.sfx_arrow_right_button_img = self.inactive_arrow_right_button_img
            self.sfx_arrow_left_button_img = self.inactive_arrow_left_button_img
            self.music_arrow_right_button_img = self.inactive_arrow_right_button_img
            self.music_arrow_left_button_img = self.inactive_arrow_left_button_img

        self.game.all_sfx["menu_hover"].set_volume(0.5 * self.game.sfx_global_volume/100)
        self.game.all_sfx["menu_click"].set_volume(0.25 * self.game.sfx_global_volume/100)
        self.game.all_music["android52 - Dancing All Night (Short)"].set_volume(self.game.music_global_volume/100)

        if self.timer < 60:
            self.timer += self.game.delta_time
            self.scale_down_button.x = int((easeOutBack(self.timer, -70, (80 + (self.game.GAME_WIDTH)//2), 60, s=1)) * self.game.SCALE)
            self.scale_up_button.x = self.scale_down_button.x + 90 * self.game.SCALE

            self.sfx_down_button.x = self.scale_down_button.x
            self.sfx_up_button.x = self.scale_down_button.x + 90 * self.game.SCALE

            self.music_down_button.x = self.scale_down_button.x
            self.music_up_button.x = self.scale_down_button.x + 90 * self.game.SCALE
            
            self.back_to_menu_button.x = int((easeOutBack(self.timer, -250, (250 + (self.game.GAME_WIDTH - 150)//2), 60, s=1)) * self.game.SCALE)
        
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])
        self.game.high_res_canvas.fill((0,0,0))

        self.options_txt.update(self.game.high_res_canvas, scale = self.game.SCALE)    
        self.scale_txt.update(self.game.high_res_canvas, content = "Tamaño de Pantalla", x = self.scale_down_button.x - 136 * self.game.SCALE, scale = self.game.SCALE)
        self.sfx_txt.update(self.game.high_res_canvas, content = "Volumen de Efectos", x = self.sfx_down_button.x - 139 * self.game.SCALE, scale = self.game.SCALE)
        self.music_txt.update(self.game.high_res_canvas, content = "Volumen de Música", x = self.music_down_button.x - 131 * self.game.SCALE, scale = self.game.SCALE)
        self.back_txt.update(self.game.high_res_canvas, x = self.back_to_menu_button.x + 75 * self.game.SCALE, scale = self.game.SCALE)

        self.scale_value_txt.update(self.game.high_res_canvas, content = str(self.game.SCREEN_WIDTH * self.game.SCALE) + "x" + str(self.game.SCREEN_HEIGHT * self.game.SCALE), x = self.scale_down_button.x + 57 * self.game.SCALE, scale = self.game.SCALE)
        self.sfx_value_txt.update(self.game.high_res_canvas, content = str(int(self.game.sfx_global_volume)) + "%", x = self.sfx_down_button.x + 60 * self.game.SCALE, scale = self.game.SCALE)
        self.music_value_txt.update(self.game.high_res_canvas, content = str(int(self.game.music_global_volume)) + "%", x = self.music_down_button.x + 60 * self.game.SCALE, scale = self.game.SCALE)

##        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.scale_up_button, width = 2)
##        pygame.draw.rect(self.game.game_canvas, colours["red"], self.scale_down_button, width = 2)
##
##        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.sfx_up_button, width = 2)
##        pygame.draw.rect(self.game.game_canvas, colours["red"], self.sfx_down_button, width = 2)
##
##        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.music_up_button, width = 2)
##        pygame.draw.rect(self.game.game_canvas, colours["red"], self.music_down_button, width = 2)

        if self.game.SCALE < self.game.MAX_SCALE:
            self.game.high_res_canvas.blit(self.scale_arrow_right_button_img, ((self.scale_up_button.x + 3 * self.game.SCALE), (self.scale_up_button.y + 3 * self.game.SCALE)))
        if self.game.SCALE > 1:
            self.game.high_res_canvas.blit(self.scale_arrow_left_button_img, ((self.scale_down_button.x + 3 * self.game.SCALE), (self.scale_down_button.y + 3 * self.game.SCALE)))

        self.game.high_res_canvas.blit(self.sfx_arrow_right_button_img, ((self.sfx_up_button.x + 3 * self.game.SCALE), (self.sfx_up_button.y + 3 * self.game.SCALE)))
        self.game.high_res_canvas.blit(self.sfx_arrow_left_button_img, ((self.sfx_down_button.x + 3 * self.game.SCALE), (self.sfx_down_button.y + 3 * self.game.SCALE)))

        self.game.high_res_canvas.blit(self.music_arrow_right_button_img, ((self.music_up_button.x + 3 * self.game.SCALE), (self.music_up_button.y + 3 * self.game.SCALE)))
        self.game.high_res_canvas.blit(self.music_arrow_left_button_img, ((self.music_down_button.x + 3 * self.game.SCALE), (self.music_down_button.y + 3 * self.game.SCALE)))
        
##        pygame.draw.rect(self.game.game_canvas, colours["red"], self.back_to_menu_button, width = 3)
        self.game.high_res_canvas.blit(self.back_to_menu_button_img, ((self.back_to_menu_button.x - 10 * self.game.SCALE), self.back_to_menu_button.y))
        

        

