import pygame, os

from scr.config.config import tiles_color_keys
from scr.config.config import entities_color_keys

from scr.config.config import colours

from scr.sprites.tile import Tile
from scr.sprites.obstacle import Barrier, Table, Box, Guard, Waiter, NPC_0, NPC_1, Goal

from scr.dialog import Dialog

class Tilemap():
    def __init__(self):

        self.TILE_WIDTH, self.TILE_HEIGHT = 20, 20
        
    def load_tiles_and_entities(self, game, tilesmap_surface, entities_surface, json_data, dialog_data):

        tiles = pygame.sprite.Group()
        entities = pygame.sprite.Group()

        dialogs = {}
        
        for key, dialog_queue in dialog_data.items():
            dialogs[key] = Dialog(game, dialog_queue, key)

        guard_counter = 1
        waiter_counter = 1

        for x in range(tilesmap_surface.get_width()):
            for y in range(tilesmap_surface.get_height()):
                for image_name, rgb in tiles_color_keys.items():
                    if image_name != "vacio" and tilesmap_surface.get_at((x,y)) == rgb:
                        # All tiles are non collidable
                        collidable = False
                        image = pygame.image.load(os.path.join("scr", "assets", "tiles", image_name))
                        image_copy = image.copy()
                        image_copy.fill(colours["black"])
                        image_copy.blit(image, (0,0))
                        tiles.add(Tile(image_copy.convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, collidable))

        for x in range(entities_surface.get_width()):
            for y in range(entities_surface.get_height()):
                for entity_name, rgb in entities_color_keys.items():
                    if entity_name != "vacio" and entities_surface.get_at((x,y)) == rgb:
                        if entity_name == "barrera":
                            image = pygame.image.load(os.path.join("scr", "assets", "images", "barrera.png"))
                            image_copy = image.copy()
                            image_copy.fill(colours["black"])
                            image_copy.blit(image, (0,0))
                            entities.add(Barrier(image_copy.convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "barrera"))
                        if entity_name == "player":
                            player_start_x = x * self.TILE_WIDTH
                            player_start_y = y * self.TILE_HEIGHT
                        if entity_name == "caja":
                            entities.add(Box(pygame.image.load(os.path.join("scr", "assets", "images", "caja.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "caja"))
                        if entity_name == "mesa":
                            entities.add(Table(pygame.image.load(os.path.join("scr", "assets", "images", "mesa.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesa"))
                        if entity_name == "guardia":
                            spawn = json_data["guardia " + str(guard_counter) + " turno spawn"]
                            radius = json_data["guardia " + str(guard_counter) + " radio vision"]
                            offset = json_data["guardia " + str(guard_counter) + " offset"]
                            entities.add(Guard(pygame.image.load(os.path.join("scr", "assets", "images", "guardia.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "guardia", [dialogs["dialog_0"], dialogs["dialog_1"],
                                                                                                                                                                                          dialogs["dialog_4"]], spawn, radius, offset))
                            guard_counter += 1
                        if entity_name == "mesero vertical":
                            direction = json_data["mesero " + str(waiter_counter) + " direccion"]
                            entities.add(Waiter(pygame.image.load(os.path.join("scr", "assets", "images", "mesero.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesero", "vertical", direction))
                            waiter_counter += 1
                        if entity_name == "mesero horizontal":
                            direction = json_data["mesero " + str(guard_counter) + " direccion"]
                            entities.add(Waiter(pygame.image.load(os.path.join("scr", "assets", "images", "mesero.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesero", "horizontal", direction))
                            waiter_counter += 1
                        if entity_name == "npc 0": # Controles de movimiento
                            entities.add(NPC_0(pygame.image.load(os.path.join("scr", "assets", "images", "invisible.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "npc", json_data["npc 0 offset"], json_data["npc 0 radio vision"]))
                        if entity_name == "npc 1": # NPC 1
                            entities.add(NPC_1(pygame.image.load(os.path.join("scr", "assets", "images", "npc.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "npc", [dialogs["dialog_5"]], json_data["npc 1 radio vision"], json_data["npc 1 offset"]))
                        if entity_name == "meta":
                            entities.add(Goal(pygame.image.load(os.path.join("scr", "assets", "images", "meta.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "meta", game))
        return tiles, entities, dialogs, player_start_x, player_start_y, (tilesmap_surface.get_width() * self.TILE_WIDTH, tilesmap_surface.get_height() * self.TILE_HEIGHT)
                        
                    
        
        
