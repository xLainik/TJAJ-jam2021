import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, img_offset):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = pygame.Rect((x, y, 20, 20))

        self.img_offset = img_offset

        if type(image) == list:
            # [{ani_1}, {ani_2}, etc]
            self.animations = image
            self.current_ani = self.animations[0]
            self.image = self.current_ani["0"]
        else:
            # single img to blit (no animation)
            self.image = image
            self.animations = None
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x + self.img_offset[0], self.rect.y + self.img_offset[1]))

    def change_frame(self, current_beat):
        for key, frame in self.current_ani.items():
            if int(key) == current_beat:
                self.image = frame
