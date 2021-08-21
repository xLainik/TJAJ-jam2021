import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, obstacle_type):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.obstable_type = obstacle_type

    def draw(self, layer):
        layer.blit(self.image, self.rect)
