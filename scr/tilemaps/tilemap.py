import pygame, os

from scr.config.config import tiles_color_keys
from scr.config.config import entities_color_keys

from scr.config.config import colours

from scr.sprites.tile import Tile
from scr.sprites.obstacle import Barrier, Table, Box, Guard, Waiter, NPC_0, NPC_2, Goal

from scr.dialog import Dialog

class Tilemap():
    def __init__(self):

        self.TILE_WIDTH, self.TILE_HEIGHT = 20, 20
        
    def load_tiles_and_entities(self, game, speed, tilesmap_surface, entities_surface, json_data, dialog_data, lvl_number):

        tiles = pygame.sprite.Group()
        entities = pygame.sprite.Group()

        dialogs = {}
        
        for key, dialog_queue in dialog_data.items():
            dialogs[key] = Dialog(game, dialog_queue, key, lvl_number, dialog_queue[str(len(dialog_queue) - 1)][4])

        guard_counter = 1
        waiter_counter = 1

        game.load_ani_tiles("piso")
        game.load_animations("guardia azul", "guardia rojo", "mesero", "meta", "npc 2")

        
        for x in range(tilesmap_surface.get_width()):
            for y in range(tilesmap_surface.get_height()):
                for tile_name, rgb in tiles_color_keys.items():
                    if tile_name != "vacio" and tilesmap_surface.get_at((x,y)) == rgb:
                        if tile_name == "piso":
                            tiles.add(Tile([game.all_tiles["piso"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0)))

        for x in range(entities_surface.get_width()):
            for y in range(entities_surface.get_height()):
                for entity_name, rgb in entities_color_keys.items():
                    if entity_name != "vacio" and entities_surface.get_at((x,y)) == rgb:
                        if entity_name == "barrera":
                            image = pygame.image.load(os.path.join("scr", "assets", "images", "barrera.png"))
                            image_copy = image.copy()
                            image_copy.fill(colours["black"])
                            image_copy.blit(image, (0,0))
                            entities.add(Barrier(image_copy.convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "barrera"))
                        if entity_name == "jugador":
                            player_start_x = x * self.TILE_WIDTH
                            player_start_y = y * self.TILE_HEIGHT

                        if entity_name == "caja":
                            entities.add(Box(pygame.image.load(os.path.join("scr", "assets", "images", "caja.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "caja", speed))
                        if entity_name == "mesa":
                            entities.add(Table(pygame.image.load(os.path.join("scr", "assets", "images", "mesa.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "mesa", speed))
                        if entity_name == "guardia":
                            spawn = json_data["guardia " + str(guard_counter) + " turno spawn"]
                            radius = json_data["guardia " + str(guard_counter) + " radio vision"]
                            offset = json_data["guardia " + str(guard_counter) + " offset"]
                            flip = bool(json_data["guardia " + str(guard_counter) + " flip"] == "True")
                            entities.add(Guard([game.all_animations["guardia azul"], game.all_animations["guardia rojo"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "guardia", [dialogs["dialog_0"], dialogs["dialog_1"],
                                                                                                                                                                                          dialogs["dialog_4"]], spawn, radius, offset, speed, flip))
                            guard_counter += 1
                        if entity_name == "mesero vertical":
                            direction = json_data["mesero " + str(waiter_counter) + " direccion"]
                            entities.add(Waiter([game.all_animations["mesero"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "mesero", "vertical", direction, speed, flip))
                            waiter_counter += 1
                        if entity_name == "mesero horizontal":
                            direction = json_data["mesero " + str(waiter_counter) + " direccion"]
                            flip = bool(json_data["mesero " + str(waiter_counter) + " flip"] == "True")
                            entities.add(Waiter([game.all_animations["mesero"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "mesero", "horizontal", direction, speed, flip))
                            waiter_counter += 1
                        if entity_name == "npc 0": # Controles de movimiento
                            entities.add(NPC_0(pygame.image.load(os.path.join("scr", "assets", "images", "invisible.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0,0), "npc", json_data["npc 0 offset"], json_data["npc 0 radio vision"]))
                        if entity_name == "npc 2": # Camarero echando carro
                            flip = bool(json_data["npc 2 flip"] == "True")
                            entities.add(NPC_2([game.all_animations["npc 2"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "npc", [dialogs["dialog_5"]], json_data["npc 2 radio vision"], json_data["npc 2 offset"], flip))
                        if entity_name == "meta":
                            entities.add(Goal([game.all_animations["meta"]], x * self.TILE_WIDTH, y * self.TILE_HEIGHT, (0, 0), "meta", game))
        return tiles, entities, dialogs, player_start_x, player_start_y, (tilesmap_surface.get_width() * self.TILE_WIDTH, tilesmap_surface.get_height() * self.TILE_HEIGHT)
                        
                    
        
        
