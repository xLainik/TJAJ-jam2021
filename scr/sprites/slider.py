import pygame

class Slider(pygame.sprite.Sprite):
    def __init__(self, blit_layer, rect) -> None:
        super().__init__()
        self.blit_layer = blit_layer

        self.rect = rect
        
    def update(self, mouse):
        
