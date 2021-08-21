import pygame

from scr.config.config import colours
from scr.tilemaps.tilemap import Tilemap

class Level():
    """Level super class"""
    def __init__(self, game, png_map, png_entities, json_data) -> None:
        self.game = game
        
        self.json_data = json_data

        tilemap = Tilemap()

        self.tiles, player_start_x, player_start_y = tilemap.load_tiles_and_entities(png_map, png_entities)

        self.game.player.level_init(player_start_x + 5, player_start_y + 5)
    
    def update(self):
        self.game.player.update(self.tiles)

    def render(self):
        self.game.game_canvas.fill(colours["black"])
        for tile in self.tiles:
            tile.draw(self.game.game_canvas)

        self.game.player.draw(self.game.game_canvas)
        
class Level_0(Level):
    def __init__(self, game, png_map, png_entities, json_data) -> None:
        super().__init__(game, png_map, png_entities, json_data)

    def update(self):
        super().update()

    def render(self):
        super().render()

