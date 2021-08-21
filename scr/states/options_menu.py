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

        self.hover = False

        self.timer = 0
        
        self.load_sprites()

        pygame.mixer.set_num_channels(2)
        
    def load_sprites(self):
        self.options_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 24, "OPTIONS", colours["white"], True, self.game.SCREEN_WIDTH//2, 28, True, self.game.SCALE)
        self.scale_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 22, "Screen Size", colours["white"], True, self.game.SCREEN_WIDTH, 54, False, self.game.SCALE)
        self.sfx_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 22, "Sound Effects", colours["white"], True, 20, 102, False, self.game.SCALE)
        self.music_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 22, "Music", colours["white"], True, 96-8, 148, False, self.game.SCALE)
        
        self.scale_down_button = pygame.Rect(-100,50,30,26)
        self.scale_up_button = pygame.Rect(-100,50,30,26)

        self.sfx_down_button = pygame.Rect(-100,98,30,26)
        self.sfx_up_button = pygame.Rect(-100,98,30,26)

        self.music_down_button = pygame.Rect(-100,144,30,26)
        self.music_up_button = pygame.Rect(-100,144,30,26)
        
        self.back_to_menu_button = pygame.Rect(-250,192,150,32)

        self.back_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 24, "BACK", colours["white"], True, self.game.SCREEN_WIDTH, 208, True, self.game.SCALE)
        
    def update(self):
        """Update the menu state."""
        self.game.check_inputs()

        mx, my = pygame.mouse.get_pos()
        mx, my = int(mx/self.game.SCALE), int(my/self.game.SCALE)

        if self.scale_up_button.collidepoint(mx, my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.SCALE += 1
                self.game.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas = pygame.Surface((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas.fill((0,0,0))
                self.game.high_res_canvas.set_colorkey((0,0,0))
                self.timer = 0
        elif self.scale_down_button.collidepoint(mx, my) and self.game.SCALE > 1:
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.SCALE -= 1
                self.game.screen = pygame.display.set_mode((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas = pygame.Surface((self.game.SCREEN_WIDTH*self.game.SCALE, self.game.SCREEN_HEIGHT*self.game.SCALE))
                self.game.high_res_canvas.fill((0,0,0))
                self.game.high_res_canvas.set_colorkey((0,0,0))
                self.timer = 0
        elif self.sfx_down_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click and self.game.sfx_global_volume > 0:
                self.game.sfx_global_volume -= 0.8
                if self.game.click == 1:
                    self.game.all_sfx["menu_click"].play()
        elif self.sfx_up_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click and self.game.sfx_global_volume < 100:
                self.game.sfx_global_volume += 0.8
                if self.game.click == 1:
                    self.game.all_sfx["menu_click"].play()
        elif self.music_down_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click and self.game.music_global_volume > 0:
                self.game.music_global_volume -= 0.8
        elif self.music_up_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click and self.game.music_global_volume < 100:
                self.game.music_global_volume += 0.8
                
        elif self.back_to_menu_button.collidepoint(mx,my):
            if not(self.hover):
                self.game.all_sfx["menu_hover"].play()
                self.hover = True
            if self.game.click:
                self.game.all_sfx["menu_click"].play()
                self.game.game_canvas.fill(colours["black"])
                self.game.state_stack[-2].timer = 0
                self.exit_state()
        else: self.hover = False

        self.game.all_sfx["menu_hover"].set_volume(0.5 * self.game.sfx_global_volume/100)
        self.game.all_sfx["menu_click"].set_volume(0.25 * self.game.sfx_global_volume/100)
        self.game.all_music["android52 - Dancing All Night (Short)"].set_volume(self.game.music_global_volume/100)

        if self.timer < 60:
            self.timer += 1
            self.scale_down_button.x = int(easeOutBack(self.timer, -70, (84 + (self.game.GAME_WIDTH)//2), 60, s=1))
            self.scale_up_button.x = self.scale_down_button.x + 84

            self.sfx_down_button.x = int(easeOutBack(self.timer, -70, (84 + (self.game.GAME_WIDTH)//2), 60, s=1))
            self.sfx_up_button.x = self.scale_down_button.x + 84

            self.music_down_button.x = int(easeOutBack(self.timer, -70, (84 + (self.game.GAME_WIDTH)//2), 60, s=1))
            self.music_up_button.x = self.scale_down_button.x + 84
            
            
            self.back_to_menu_button.x = int(easeOutBack(self.timer, -250, (250 + (self.game.GAME_WIDTH - 150)//2), 60, s=1))
        
            
    def render(self):
        """Render the menu state."""
        self.game.game_canvas.fill(colours["black"])
        self.game.high_res_canvas.fill((0,0,0))

        self.options_txt.update(self.game.high_res_canvas, scale = self.game.SCALE)    
        self.scale_txt.update(self.game.high_res_canvas, content = "Screen Size                 x" + str(self.game.SCALE), x = self.scale_down_button.x - 128+14, scale = self.game.SCALE)
        self.sfx_txt.update(self.game.high_res_canvas, content = "Sound Efects Vol.              " + str(int(self.game.sfx_global_volume)) + "%", x = self.sfx_down_button.x - 160, scale = self.game.SCALE)
        self.music_txt.update(self.game.high_res_canvas, content = "Music Vol.               " + str(int(self.game.music_global_volume)) + "%", x = self.music_down_button.x - 112+6, scale = self.game.SCALE)
        self.back_txt.update(self.game.high_res_canvas, x = self.back_to_menu_button.x + 78, scale = self.game.SCALE)
        
        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.scale_up_button, width = 2)
        pygame.draw.rect(self.game.game_canvas, colours["red"], self.scale_down_button, width = 2)

        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.sfx_up_button, width = 2)
        pygame.draw.rect(self.game.game_canvas, colours["red"], self.sfx_down_button, width = 2)

        pygame.draw.rect(self.game.game_canvas, colours["blue"], self.music_up_button, width = 2)
        pygame.draw.rect(self.game.game_canvas, colours["red"], self.music_down_button, width = 2)
        
        pygame.draw.rect(self.game.game_canvas, colours["white"], self.back_to_menu_button, width = 4)
        

        

