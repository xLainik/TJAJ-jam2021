import pygame, math

class Camera:
    def __init__(self, player, level_surface, game) -> None:
        self.player_rect = player.rect
        self.level_width, self.level_height = level_surface.get_width(), level_surface.get_height()

        self.rect = pygame.Rect(self.player_rect.centerx - game.SCREEN_WIDTH//2, self.player_rect.centery - game.SCREEN_HEIGHT//2, game.SCREEN_WIDTH, game.SCREEN_HEIGHT)

        self.speed_x, self.speed_y = 0, 0
        
        # Level borders
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width

        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.level_height: self.rect.bottom = self.level_height

    def update(self, player):
        self.rect.center = player.rect.center

        # Level borders
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width

        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.level_height: self.rect.bottom = self.level_height
