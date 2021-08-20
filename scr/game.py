import pygame, time, os, sys
from scr.config.config import options, colours
from scr.states.main_menu import Main_menu

class Game:
    """The game object, used to control the game."""
    def __init__(self) -> None:
        """Initializing the game."""
        #pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.display.set_caption(options["window_title"])
        
        self.SCALE = options["scale"]
        
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = options["game_width"], options["game_height"]
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH*self.SCALE, self.SCREEN_HEIGHT*self.SCALE))

        icon_img = pygame.image.load(os.path.join("scr", "assets", "icon.png")).convert()
        pygame.display.set_icon(icon_img)
        
        self.GAME_SIZE = self.GAME_WIDTH, self.GAME_HEIGHT = options["game_width"], options["game_height"]
        self.game_canvas = pygame.Surface(self.GAME_SIZE)
        self.clock = pygame.time.Clock()
        self.MAX_FPS = options["fps"]
        self.running, self.playing = True, True

        self.delta_time, self.previous_time = 0, 0
        self.state_stack = []

        self.click = False

        pygame.mixer.set_num_channels(5)

    def new(self):
        """Starting a new game"""
        self.setup_directories()
        self.load_first_state()
        self.game_loop()

    def restart(self):
        self.__init__
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

    def render(self):
        """Renders the needed opponents according to the current game state."""
        self.state_stack[-1].render()

        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH*self.SCALE, self.SCREEN_HEIGHT*self.SCALE)), (0, 0))
        pygame.display.update()
        self.clock.tick(self.MAX_FPS)

    def check_inputs(self) -> None:
        """Checking for inputs from the user."""
        self.actions = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = False


    def load_first_state(self) -> None:
        """Loading the first state of the game."""
        self.state_stack = [Main_menu(self)]

    def get_delta_time(self) -> None:
        """Getting the time used between frames. Used to calculate movement so its universal across frame rates."""
        now = time.time()
        self.delta_time = now - self.previous_time
        self.delta_time *= self.MAX_FPS
        self.previous_time = now

    def load_animations(self, *animation_list):
        """Loads just the animations needed at the moment."""
        self.all_animations = {}
        for animations in os.listdir(self.game.animation_directory):
            if animations in animation_list:
                self.all_animations[animations] = []
                for frames in os.listdir(os.path.join(self.game.animation_directory, animations)):
                    img = pygame.image.load(os.path.join(self.game.animation_directory, animations, frames)).convert()
                    img.set_colorkey((0,0,0))
                    duration = frames.split("_")[-1].split(".")[0]
                    self.all_animations[animations].append([img, int(duration)])

    def load_sounds(self, *sound_list):
        """Loads just the sounds needed at the moment."""
        self.all_sounds = {}
        for sound in os.listdir(self.sound_directory):
            if sound in sound_list:
                self.all_sounds[sound.split(".")[0]] = pygame.mixer.Sound(os.path.join(self.sound_directory, sound))

    def setup_directories(self) -> None:
        self.state_directory = os.path.join("scr", "states")
        self.level_directory = os.path.join("scr", "levels")
        
        
        self.asset_directory = os.path.join("scr", "assets")
        self.font_directory = os.path.join(self.asset_directory, "fonts")
        self.tile_directory = os.path.join(self.asset_directory, "tiles")
        self.image_directory = os.path.join(self.asset_directory, "images")
        self.animation_directory = os.path.join(self.asset_directory, "animations")
        self.sound_directory = os.path.join(self.asset_directory, "sounds")
        
    def shut_down(self) -> None:
        """Completley shutting down the game."""
        self.playing = False
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()