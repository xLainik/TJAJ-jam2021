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
        
        tilemap = Tilemap()

        self.level_number = level_number

        self.tiles, self.entities, self.dialogs, player_start_x, player_start_y, self.LEVEL_SIZE = tilemap.load_tiles_and_entities(game, png_map, png_entities, self.json_data, dialog_data)

        self.tiles_surface = pygame.Surface((self.LEVEL_SIZE))

        self.tiles_surface.set_colorkey((0, 0, 0))
        self.tiles_surface.fill((0, 0, 0))

        self.entities_surface = pygame.Surface((self.LEVEL_SIZE))

        self.entities_surface.set_colorkey((0, 0, 0))
        self.entities_surface.fill((0, 0, 0))

        if self.level_number == self.game.current_level:
            self.game.player.level_init(player_start_x + 5, player_start_y + 5)
        self.entities.add(self.game.player)

        self.guards = pygame.sprite.Group()

        for entity in self.entities:
            if entity.entity_name != "player" and entity.entity_name != "barrera" and entity.entity_name != "meta" and entity.entity_name != "npc" and entity.entity_name != "mesero" and  entity.entity_name != "guardia":
                entity.calculate_push(self.entities)
            elif entity.entity_name == "guardia":
                entity.create_maze(self.entities, self.game.player.rect)
                self.guards.add(entity)

        self.camera = Camera(self.game.player, self.tiles_surface, self.game)
        self.camera_surface = pygame.Surface((self.game.SCREEN_SIZE))

        self.camera_surface.set_colorkey((0, 0, 0))
        self.camera_surface.fill((0, 0, 0))

        self.player_turn = False
        self.player_turn_timer = 0

        self.guards_turn_timer = 0
        
        self.turn_counter = 0
    
    def update(self):
        # player turn
        if self.player_turn:
            if self.player_turn_timer == 0:
                self.game.player.update(self.entities, self.game.delta_time)
            if self.game.player.can_move == False:
                self.player_turn_timer += self.game.delta_time
                for entity in self.entities:
                    if entity.entity_name != "guardia":
                        entity.update(self.entities, self.game.delta_time)
                        if entity.entity_name == "npc":
                            entity.check_action(self.game.player.rect)
            if self.player_turn_timer >= 16:
                self.player_turn = False
                self.player_turn_timer = 0
                for entity in self.entities:
                    if entity.entity_name != "guardia" and entity.entity_name != "meta" and entity.entity_name != "barrera" and entity.entity_name != "npc":
                        if entity.entity_name == "mesa" and entity.moving == True:
                            entity.standing = False
                            entity.push_directions = {"left": False, "right": False, "down": False, "up": False}
                        entity.moving = False
                        entity.speed_x, entity.speed_y = 0, 0
                        entity.x = entity.rect.x = entity.move_destination[0]
                        entity.y = entity.rect.y = entity.move_destination[1]
                            

        # Guards turn
        if not(self.player_turn):
            # Enter the turn
            if self.guards_turn_timer == 0:
##                print("- GUARDS'S TURN")
                for guard in self.guards:
                    guard.enter_turn(self.entities, self.game.player.rect)
            counter = 0
            for guard in self.guards:
                if guard.active:
                    guard.update(self.entities, self.game.delta_time)
                elif guard.spawn_turn == self.turn_counter:
                    guard.active = True
                if guard.moves == False:
                    counter += 1
            if counter >= len(self.guards.sprites()) and self.guards_turn_timer < 10: self.guards_turn_timer = 10
            self.guards_turn_timer += self.game.delta_time
            if self.guards_turn_timer >= 16:
                self.player_turn = True
                self.game.player.can_move = True
                self.turn_counter += 1
##                print("# PLAYER'S TURN " + str(self.turn_counter))
                self.guards_turn_timer = 0
                for entity in self.entities:
                    if entity.entity_name != "guardia":
                        entity.enter_turn(self.entities, self.game.player.rect)
                for guard in self.guards:
                    if guard.active:
                        guard.moving = False
                        guard.speed_x, guard.speed_y = 0, 0
                        guard.x = guard.rect.x = guard.move_destination[0]
                        guard.y = guard.rect.y = guard.move_destination[1]

        

        for key, dialog in self.dialogs.items():
            if dialog.active:
                dialog.update()
                if self.game.player.dead:
                    break

        if self.game.player.dead:
            self.game.state_stack[-1].restart_level()
           
        self.camera.update(self.game.player)

##        if self.game.actions["escape"]:
##            pause = Pause(self.game)
##            pause.enter_state()

    def render(self):
        self.tiles_surface.fill((0, 0, 0), rect=self.camera.rect)
    
        for tile in self.tiles:
            tile.draw(self.tiles_surface)

        self.entities_surface.fill((0,0,0), rect=self.camera.rect)

        for entity in self.entities:
            entity.draw(self.entities_surface)

        self.camera_surface.blit(self.tiles_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))
        self.camera_surface.blit(self.entities_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))

        self.game.game_canvas.blit(self.camera_surface, (0, 0))
        
class Level_0(Level):
    def __init__(self, game, png_map, png_entities, json_data, dialog_data, lvl_number) -> None:
        super().__init__(game, png_map, png_entities, json_data, dialog_data, lvl_number)

    def update(self):
        super().update()

    def render(self):
        super().render()

class Level_1(Level):
    def __init__(self, game, png_map, png_entities, json_data, dialog_data, lvl_number) -> None:
        super().__init__(game, png_map, png_entities, json_data, dialog_data, lvl_number)

    def update(self):
        super().update()

    def render(self):
        super().render()

