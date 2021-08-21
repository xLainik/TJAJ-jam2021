import pygame, os

from scr.config.config import tiles_color_keys
from scr.config.config import entities_color_keys

from scr.sprites.tile import Tile
from scr.sprites.obstacle import Obstacle

class Tilemap():
    def __init__(self):

        self.TILE_WIDTH, self.TILE_HEIGHT = 20, 20
        

    def load_tiles_and_entities(self, tilesmap_surface, entities_surface):

        tiles = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()

        for x in range(tilesmap_surface.get_width()):
            for y in range(tilesmap_surface.get_height()):
                for image_name, rgb in tiles_color_keys.items():
                    if image_name != "vacio" and tilesmap_surface.get_at((x,y)) == rgb:
                        # Check for collidable tiles or not
                        if image_name == "barrera.png": collidable = True
                        else: collidable = False
                        tiles.add(Tile(pygame.image.load(os.path.join("scr", "assets", "tiles", image_name)).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, collidable))

        for x in range(entities_surface.get_width()):
            for y in range(entities_surface.get_height()):
                for entity_name, rgb in entities_color_keys.items():
                    if entity_name != "vacio" and entities_surface.get_at((x,y)) == rgb:
                        if entity_name == "player":
                            player_start_x = x * self.TILE_WIDTH
                            player_start_y = y * self.TILE_HEIGHT
                        if entity_name == "caja":
                            obstacles.add(Obstacle(pygame.image.load(os.path.join("scr", "assets", "images", "caja.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "caja"))
                        if entity_name == "mesa":
                            obstacles.add(Obstacle(pygame.image.load(os.path.join("scr", "assets", "images", "mesa.png")).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT, "mesa"))
                        
        return tiles, obstacles, player_start_x, player_start_y, (tilesmap_surface.get_width() * self.TILE_WIDTH, tilesmap_surface.get_height() * self.TILE_HEIGHT)
                        
                    
        
        
