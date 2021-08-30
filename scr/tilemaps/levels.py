import pygame

from scr.config.config import colours
from scr.tilemaps.tilemap import Tilemap

from scr.camera import Camera

from scr.states.pause import Pause

class Level():
    """Level super class"""
    def __init__(self, game, png_map, png_entities, json_data, dialog_data, level_number) -> None:
        self.game = game

        self.game.transition_timer = -1
        
        self.json_data = json_data
        

        self.BPM, self.speed = 0, 0

        self.timer_active = False

        self.turn_counter = 0
        self.player_turn = True
        self.player_enter_turn = False
        self.guards_enter_turn = False
    
    def update(self):

        # Cheacker si el player cagó
        self.game.player.check_inputs(self.player_turn)

        # Checkear que el input del jugador está en el ritmo correcto
        if self.game.beat_counter in [0, 1, 2, 7]:
            if self.player_enter_turn and self.game.player.miss_beat == False:
                self.game.player.can_move = True
                self.player_enter_turn = False

            if self.game.beat_counter == 2:
                self.game.player.miss_beat = False
                self.player_turn = False

            for entity in self.entities:
                if entity.entity_name != "player":
                    entity.update(self.entities, self.game.delta_time)

            if self.game.beat_counter in [0, 1, 7]:
                self.player_turn = True
                self.game.player.update(self.entities, self.game.delta_time)

                self.guards_enter_turn = False

            # Iniciar timer                 
            if self.game.player.moving and not(self.timer_active):
                self.game.player.can_move = True
                self.game.enter_beat = True
                self.game.play_beat = True
                pygame.time.set_timer(self.game.BEAT_EVENT, int((60/self.BPM)*1000/4))
                self.timer_active = True
        
        if self.game.beat_counter == 3:
            # Enter the Guards turn
            if self.guards_enter_turn == False:
                # Correct entities position first to avoid errors
                for entity in self.entities:
                    if entity.entity_name != "guardia" and entity.entity_name != "meta" and entity.entity_name != "barrera" and entity.entity_name != "npc":
                        if entity.entity_name == "mesa" and entity.moving == True:
                            entity.standing = False
                            entity.push_directions = {"left": False, "right": False, "down": False, "up": False}
                        entity.moving = False
                        entity.speed_x, entity.speed_y = 0, 0
                        entity.x = entity.rect.x = entity.move_destination[0]
                        entity.y = entity.rect.y = entity.move_destination[1]
                self.guards_enter_turn = True
                self.turn_counter += 1
                for guard in self.guards:
                    guard.enter_turn(self.entities, self.game.player.rect)
        
        # Guards' TURN
        if self.game.beat_counter in [4, 5]:        
            for guard in self.guards:
                if  guard.active:
                    guard.update(self.entities, self.game.delta_time)
                elif guard.spawn_turn == self.turn_counter:
                    guard.active = True
                    guard.create_maze(self.entities, self.game.player.rect)

            self.player_enter_turn = False
            

        if self.game.beat_counter == 6:
            # Enter the Player's / Entities' turn
            if self.player_enter_turn == False:
                self.player_enter_turn = True
                for entity in self.entities:
                    if entity.entity_name != "guardia":
                        entity.enter_turn(self.entities, self.game.player.rect)

        # Marcar el ritmo con sonidos
        if self.drum_beat[self.game.beat_counter] != None:
            if self.game.enter_beat:
                self.drum_beat[self.game.beat_counter].play()
                self.game.enter_beat = False


        for key, dialog in self.dialogs.items():
            if dialog.active:
                dialog.update()
                if self.game.player.dead:
                    break

        # Condición de perder
        if self.game.player.dead:
            self.game.player.miss_beat = False
            self.game.enter_beat = False
            self.game.play_beat = False
            self.game.beat_counter = 0
            pygame.time.set_timer(self.game.BEAT_EVENT, 0)
            self.game.state_stack[-1].restart_level()
           
        self.camera.update(self.game.player)

##        if self.game.actions["escape"]:
##            pause = Pause(self.game)
##            pause.enter_state()

    def render(self):
        self.game.game_canvas.fill((0, 0, 0))
        
        self.tiles_surface.fill((0, 0, 0), rect=self.camera.rect)
    
        for tile in self.tiles:
            tile.draw(self.tiles_surface)

        self.entities_surface.fill((0,0,0), rect=self.camera.rect)

        self.game.player.draw(self.entities_surface)

        for entity in self.entities:
            entity.draw(self.entities_surface)

        self.camera_surface.fill((0, 0, 0))

        self.camera_surface.blit(self.tiles_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))
        self.camera_surface.blit(self.entities_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))

        self.game.game_canvas.blit(self.camera_surface, (0, 0))
        
class Level_1(Level):
    def __init__(self, game, png_map, png_entities, json_data, dialog_data, level_number) -> None:
        super().__init__(game, png_map, png_entities, json_data, dialog_data, level_number)

        self.game.load_sfx("kick_2.wav", "shaker_2.wav", "clap_2.wav")

        self.game.all_sfx["kick_2"].set_volume(self.game.sfx_global_volume/100)
        self.game.all_sfx["shaker_2"].set_volume(0.5 * self.game.sfx_global_volume/100)
        self.game.all_sfx["clap_2"].set_volume(self.game.sfx_global_volume/100)    
    
        clap = self.game.all_sfx["clap_2"]
        kick = self.game.all_sfx["kick_2"]
        shaker = self.game.all_sfx["shaker_2"]
        
        # First bar: player                         second bar: Guard
        self.drum_beat = [kick, None, shaker, None, clap, None, shaker, None]

        self.BPM = 103
        self.speed = 20 / (30*self.game.MAX_FPS / self.BPM)
        self.game.beat_counter = 0
        

        tilemap = Tilemap()

        self.level_number = level_number

        self.tiles, self.entities, self.dialogs, player_start_x, player_start_y, self.LEVEL_SIZE = tilemap.load_tiles_and_entities(game, self.speed*3, png_map, png_entities, self.json_data, dialog_data)

        self.tiles_surface = pygame.Surface((self.LEVEL_SIZE))

        self.tiles_surface.set_colorkey((0, 0, 0))
        self.tiles_surface.fill((0, 0, 0))

        self.entities_surface = pygame.Surface((self.LEVEL_SIZE))

        self.entities_surface.set_colorkey((0, 0, 0))
        self.entities_surface.fill((0, 0, 0))

        self.guards = pygame.sprite.Group()
        
        if self.level_number == self.game.current_level:
            self.game.player.level_init(player_start_x + 5, player_start_y + 5, self.speed*2)
            self.entities.add(self.game.player)

        for entity in self.entities:
            if entity.entity_name != "player" and entity.entity_name != "barrera" and entity.entity_name != "meta" and entity.entity_name != "npc" and entity.entity_name != "mesero" and  entity.entity_name != "guardia":
                entity.calculate_push(self.entities)
            elif entity.entity_name == "guardia":
                if entity.spawn_turn == self.turn_counter:
                    entity.active = True
                    entity.create_maze(self.entities, self.game.player.rect)
                self.guards.add(entity)

        self.camera = Camera(self.game.player, self.tiles_surface, self.game)
        self.camera_surface = pygame.Surface((self.game.SCREEN_SIZE))

        self.camera_surface.set_colorkey((0, 0, 0))
        self.camera_surface.fill((0, 0, 0))

    def update(self):
        super().update()

    def render(self):
        super().render()

class Level_2(Level):
    def __init__(self, game, png_map, png_entities, json_data, dialog_data, lvl_number) -> None:
        super().__init__(game, png_map, png_entities, json_data, dialog_data, lvl_number)

    def update(self):
        super().update()

    def render(self):
        super().render()

