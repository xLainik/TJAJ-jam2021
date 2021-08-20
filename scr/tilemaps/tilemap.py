import pygame, os

from scr.config.config import tiles_color_keys

from scr.sprites.tile import Tile

class Tilemap():
    def __init__(self):

        self.TILE_WIDTH, self.TILE_HEIGHT = 20, 20
        

    def load_tiles_and_entities(self, tilesmap_surface):

        tiles = pygame.sprite.Group()

        for x in range(tilesmap_surface.get_width()):
            for y in range(tilesmap_surface.get_height()):
                for image_name, rgb in tiles_color_keys.items():
                    if image_name != "vacio" and tilesmap_surface.get_at((x,y)) == rgb:
                        tiles.add(Tile(pygame.image.load(os.path.join("scr", "assets", "tiles", image_name)).convert(), x * self.TILE_WIDTH, y * self.TILE_HEIGHT))


        return tiles
                        
                    
        
        
