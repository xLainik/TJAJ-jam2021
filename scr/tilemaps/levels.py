import pygame

from scr.config.config import tiles_color_keys
from scr.config.config import colours
from scr.tilemaps.tilemap import Tilemap

class Level():
    """Level super class"""
    def __init__(self, game, png_map, json_data) -> None:
        self.game = game
        
        self.json_data = json_data

        tilemap = Tilemap()

        self.tiles = tilemap.load_tiles_and_entities(png_map)
    
    def update(self):
        pass

    def render(self):
        self.game.game_canvas.fill(colours["black"])
        for tile in self.tiles:
            tile.draw(self.game.game_canvas)
        
class Level_0(Level):
    def __init__(self, game, png_map, json_data) -> None:
        super().__init__(game, png_map, json_data)

    def update(self):
        super().update()

    def render(self):
        super().render()
