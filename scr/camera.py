import pygame, math

class Camera:
    def __init__(self, player, level_surface, game) -> None:
        self.player_rect = player.rect
        self.level_width, self.level_height = level_surface.get_width(), level_surface.get_height()

        self.speed_x, self.speed_y = 0, 0

        self.rect = pygame.Rect(self.player_rect.centerx - game.SCREEN_WIDTH//2, self.player_rect.centery - game.SCREEN_HEIGHT//2, game.SCREEN_WIDTH, game.SCREEN_HEIGHT)

        # Level borders
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.level_width: self.rect.right = self.level_width

        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.level_height: self.rect.bottom = self.level_height

        self.horizontal_scroll, self.vertical_scroll = True, True
        
        # Level tinner than camera in the X axis
        if self.level_width + 1 < game.SCREEN_WIDTH:
            self.horizontal_scroll = False
            self.rect.centerx = level_surface.get_rect().centerx
        # Level shorter that camera in the Y axis
        if self.level_height + 1 < game.SCREEN_HEIGHT:
            self.vertical_scroll = False
            self.rect.centery = level_surface.get_rect().centery
        

    def update(self, player):

        if self.horizontal_scroll:
            self.rect.centerx = player.rect.centerx
            # Level borders
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > self.level_width: self.rect.right = self.level_width
        if self.vertical_scroll:
            self.rect.centery = player.rect.centery
            # Level borders
            if self.rect.top < 0: self.rect.top = 0
            if self.rect.bottom > self.level_height: self.rect.bottom = self.level_height
