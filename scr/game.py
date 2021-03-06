import pygame, time, os, sys, json

from pygame._sdl2.video import Window

from scr.config.config import options, colours
from scr.states.main_menu import Main_menu

from scr.sprites.player import Player

class Game:
    """The game object, used to control the game."""
    def __init__(self) -> None:
        """Initializing the game."""
        pygame.init()
        pygame.display.set_caption(options["window_title"])
        
        self.SCALE = options["scale"]
        
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = options["game_width"], options["game_height"]
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH * self.SCALE, self.SCREEN_HEIGHT * self.SCALE))

        self.MONITOR_SIZE = (pygame.display.list_modes(depth=0, flags=pygame.FULLSCREEN, display=0)[0][0], pygame.display.list_modes(depth=0, flags=pygame.FULLSCREEN, display=0)[0][1])

        self.MAX_SCALE = int(self.MONITOR_SIZE[0] / self.SCREEN_WIDTH)
        if self.MAX_SCALE > 4: self.MAX_SCALE = 4

        self.window = Window.from_display_module()
        # Center the window on the screen no matter the screen scale choosen
        self.window.position = (int(self.MONITOR_SIZE[0]/2 - (self.SCREEN_WIDTH * self.SCALE / 2)), int(self.MONITOR_SIZE[1]/2 - (self.SCREEN_HEIGHT * self.SCALE / 2)))

        self.high_res_canvas = pygame.Surface((self.SCREEN_WIDTH * self.SCALE, self.SCREEN_HEIGHT * self.SCALE))
        self.high_res_canvas.fill((0,0,0))
        self.high_res_canvas.set_colorkey((0,0,0))

        icon_img = pygame.image.load(os.path.join("scr", "assets", "icon.png")).convert()
        pygame.display.set_icon(icon_img)
        
        self.GAME_SIZE = self.GAME_WIDTH, self.GAME_HEIGHT = options["game_width"], options["game_height"]
        self.game_canvas = pygame.Surface(self.GAME_SIZE)
        self.clock = pygame.time.Clock()
        self.MAX_FPS = options["fps"]

        self.transition_timer = -1
        
        self.running, self.playing = True, True

        self.delta_time, self.previous_time = 0, 0
        self.state_stack = []

        self.click = 0

        self.setup_directories()

        self.load_animations("jugador")
        self.player = Player(self, [self.all_animations["jugador"]], 0, 0, (-5, -15))

        self.current_level = options["current_level"]

        self.BEAT_EVENT = pygame.USEREVENT + 1

        self.play_beat = False
        
        self.beat_counter = 0
        self.enter_beat = False

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, self.BEAT_EVENT])

        self.actions = {"up": False, "down": False, "left": False, "right":False, "space": False, "r": False, "escape": False}

        pygame.mixer.set_num_channels(5)
        self.sfx_global_volume = options["sfx_volumen"]
        self.music_global_volume = options["music_volumen"]

    def new(self):
        """Starting a new game"""
        self.setup_directories()
        self.load_first_state()
        self.game_loop()

    def restart(self):
        print(self.current_level)
        self.save_settings()
        self.__init__()
        self.new()

    def game_loop(self) -> None:
        """The main game loop, used to update the game based on inputs and then rendering it on the screen."""
        while self.playing:
            self.get_delta_time()
            self.check_inputs()
            self.update()
            self.render()

    def update(self) -> None:
        """Updates the needed opponents according to the current game state with respect for the imputs recived."""
        self.state_stack[-1].update()

##        if not(pygame.mouse.get_focused()):
##            print("AIUDAAA")

    def render(self):
        """Renders the needed opponents according to the current game state."""
        self.state_stack[-1].render()
        
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH * self.SCALE, self.SCREEN_HEIGHT * self.SCALE)), (0, 0))
        self.screen.blit(self.high_res_canvas, (0,0))
        self.transition_screen()
        pygame.display.update()
        self.clock.tick(self.MAX_FPS)

    def transition_screen(self):
        if self.transition_timer >= 0:
            self.transition_timer += self.delta_time
            self.transition_img = pygame.Surface((self.SCREEN_WIDTH*self.SCALE, self.SCREEN_HEIGHT*self.SCALE))
            # 0 <- fade in -> 26 <- complete darkness -> 52 <- fade out -> 78
            if self.transition_timer <= 26:
                alpha = int(255*(self.transition_timer/26))
                self.transition_img.set_alpha(alpha)
            elif self.transition_timer <= 52:
                alpha = 255
                self.transition_img.set_alpha(alpha)
            elif self.transition_timer <= 78:
                alpha = int(255*(1 - (self.transition_timer - 52)/26))
                self.transition_img.set_alpha(alpha)
            self.screen.blit(self.transition_img, (0,0))
            if self.transition_timer > 76: self.transition_timer = -1

    def check_inputs(self) -> None:
        """Checking for inputs from the user."""

        self.actions["up"] = self.actions["down"] = self.actions["left"] = self.actions["right"] = self.actions["space"] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.actions["up"] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.actions["down"] = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.actions["left"] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.actions["right"] = True
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
                if event.key == pygame.K_r:
                    self.actions["r"] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.actions["r"] = False
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = False
            if self.play_beat and event.type == self.BEAT_EVENT:
                self.enter_beat = True
                
                if self.beat_counter == 7:
                    self.beat_counter = 0
                else:
                    self.beat_counter += 1
                    

    def load_first_state(self) -> None:
        """Loading the first state of the game."""
        self.state_stack = [Main_menu(self, True)]

    def get_delta_time(self) -> None:
        """Getting the time used between frames. Used to calculate movement so its universal across frame rates."""
        now = time.time()
        self.delta_time = now - self.previous_time
        self.delta_time *= self.MAX_FPS
        self.previous_time = now

    def load_animations(self, *animation_list):
        """Loads just the animations needed at the moment."""
        self.all_animations = {}
        for animation in os.listdir(self.animation_directory):
            if animation in animation_list:
                ani_dict = {}
                for frame in os.listdir(os.path.join(self.animation_directory, animation)):
                    img = pygame.image.load(os.path.join(self.animation_directory, animation, frame)).convert()
                    img.set_colorkey((0,0,0))
                    duration = frame.split("_")[-1].split(".")[0]
                    ani_dict[str(duration)] = img
                self.all_animations[animation] = ani_dict

    def load_full_animations(self, *animation_list):
        """Loads non-frame restricted animations (for particles and effects)."""
        self.all_full_animations = {}
        for animations in os.listdir(self.animation_directory):
            if animations in animation_list:
                self.all_full_animations[animations] = []
                for frames in os.listdir(os.path.join(self.animation_directory, animations)):
                    img = pygame.image.load(os.path.join(self.animation_directory, animations, frames)).convert()
                    img.set_colorkey((0,0,0))
                    duration = frames.split("_")[-1].split(".")[0]
                    self.all_full_animations[animations].append([img, int(duration)])

    def load_ani_tiles(self, *animation_list):
        self.all_tiles = {}
        for ani_tile in os.listdir(self.tile_directory):
            if ani_tile in animation_list:
                ani_dict = {}
                for frame in os.listdir(os.path.join(self.tile_directory, ani_tile)):
                    img = pygame.image.load(os.path.join(self.tile_directory, ani_tile, frame)).convert()
                    img.set_colorkey((0,0,0))
                    duration = frame.split("_")[-1].split(".")[0]
                    ani_dict[str(duration)] = img
                self.all_tiles[ani_tile] = ani_dict

    def load_music(self, *music_list):
        """Loads just the songs needed at the moment."""
        self.all_music = {}
        for sound in os.listdir(self.music_directory):
            if sound in music_list:
                self.all_music[sound.split(".")[0]] = pygame.mixer.Sound(os.path.join(self.music_directory, sound))

    def load_sfx(self, *sfx_list):
        """Loads just the sound effects needed at the moment."""
        self.all_sfx = {}
        for sound in os.listdir(self.sfx_directory):
            if sound in sfx_list:
                self.all_sfx[sound.split(".")[0]] = pygame.mixer.Sound(os.path.join(self.sfx_directory, sound))

    def setup_directories(self) -> None:
        self.state_directory = os.path.join("scr", "states")
        self.level_directory = os.path.join("scr", "levels")
        
        self.asset_directory = os.path.join("scr", "assets")
        self.font_directory = os.path.join(self.asset_directory, "fonts")
        self.tile_directory = os.path.join(self.asset_directory, "tiles")
        self.image_directory = os.path.join(self.asset_directory, "images")
        self.animation_directory = os.path.join(self.asset_directory, "animations")
        
        self.sound_directory = os.path.join(self.asset_directory, "sounds")
        self.sfx_directory = os.path.join(self.sound_directory, "sfx")
        self.music_directory = os.path.join(self.sound_directory, "music")

    def save_settings(self) -> None:
        # Saving some settings and progress before closing the game

        with open(os.path.join("scr", "config", "options.json"), "r") as options_json_file:
            new_options = json.load(options_json_file)
    
            new_options["scale"] = self.SCALE
            new_options["sfx_volumen"] = self.sfx_global_volume
            new_options["music_volumen"] = self.music_global_volume
            new_options["current_level"] = self.current_level
            
            options_json_file.close()
            
        with open(os.path.join("scr","config", "options.json"), "w") as options_json_file:
            json.dump(new_options, options_json_file)
            options_json_file.close()
        
    def shut_down(self) -> None:
        """Completley shutting down the game."""
        self.playing = False
        self.running = False

        self.save_settings()
        
        pygame.display.quit()
        pygame.quit()
        sys.exit()
