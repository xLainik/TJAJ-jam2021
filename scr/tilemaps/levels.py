import pygame

from scr.config.config import colours
from scr.tilemaps.tilemap import Tilemap

from scr.camera import Camera

class Level():
    """Level super class"""
    def __init__(self, game, png_map, png_entities, json_data) -> None:
        self.game = game
        
        self.json_data = json_data

        tilemap = Tilemap()

        self.tiles, self.obstacles, player_start_x, player_start_y, self.LEVEL_SIZE = tilemap.load_tiles_and_entities(png_map, png_entities)

        self.tiles_surface = pygame.Surface((self.LEVEL_SIZE))

        self.tiles_surface.set_colorkey((0, 0, 0))
        self.tiles_surface.fill((0, 0, 0))

        self.entities_surface = pygame.Surface((self.LEVEL_SIZE))

        self.entities_surface.set_colorkey((0, 0, 0))
        self.entities_surface.fill((0, 0, 0))

        self.game.player.level_init(player_start_x + 5, player_start_y + 5)

        self.camera = Camera(self.game.player, self.tiles_surface, self.game)
        self.camera_surface = pygame.Surface((self.game.SCREEN_SIZE))

        self.camera_surface.set_colorkey((0, 0, 0))
        self.camera_surface.fill((0, 0, 0))

        self.level_turn = ["player", "enemies"]
    
    def update(self):
        self.game.player.update(self.tiles)
        self.camera.update(self.game.player)

    def render(self):
        self.tiles_surface.fill(colours["black"], rect=self.camera.rect)
    
        for tile in self.tiles:
            tile.draw(self.tiles_surface)

        self.entities_surface.fill((0,0,0), rect=self.camera.rect)

        for obstacle in self.obstacles:
            obstacle.draw(self.entities_surface)

        self.game.player.draw(self.entities_surface)

        self.camera_surface.blit(self.tiles_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))
        self.camera_surface.blit(self.entities_surface, (0,0), area=(self.camera.rect.x, self.camera.rect.y, self.camera.rect.width, self.camera.rect.height))

        self.game.game_canvas.blit(self.camera_surface, (0, 0))
        
class Level_0(Level):
    def __init__(self, game, png_map, png_entities, json_data) -> None:
        super().__init__(game, png_map, png_entities, json_data)

    def update(self):
        super().update()

    def render(self):
        super().render()

