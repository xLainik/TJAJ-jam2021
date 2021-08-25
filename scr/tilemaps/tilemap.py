import pygame, os

from scr.config.config import tiles_color_keys
from scr.config.config import entities_color_keys

from scr.config.config import colours

from scr.sprites.tile import Tile
from scr.sprites.obstacle import Barrier, Table, Box, Guard, Waiter

class Tilemap():
    def __init__(self):

        self.TILE_WIDTH, self.TILE_HEIGHT = 20, 20
        
    def load_tiles_and_entities(self, tilesmap_surface, entities_surface, json_data):

        tiles = pygame.sprite.Group()
        entities = pygame.sprite.Group()

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
                            entities.add(Guard(pygame.image.load(os.path.join("scr", "assets", "images", "guardia.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "guardia", spawn, radius))
                            guard_counter += 1
                        if entity_name == "mesero vertical":
                            direction = json_data["mesero " + str(waiter_counter) + " direccion"]
                            entities.add(Waiter(pygame.image.load(os.path.join("scr", "assets", "images", "mesero.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesero", "vertical", direction))
                            waiter_counter += 1
                        if entity_name == "mesero horizontal":
                            direction = json_data["mesero " + str(guard_counter) + " direccion"]
                            entities.add(Waiter(pygame.image.load(os.path.join("scr", "assets", "images", "mesero.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesero", "horizontal", direction))
                            waiter_counter += 1
        return tiles, entities, player_start_x, player_start_y, (tilesmap_surface.get_width() * self.TILE_WIDTH, tilesmap_surface.get_height() * self.TILE_HEIGHT)
                        
                    
        
        
