import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, blit_layer, font_path: str, font_size: int, content: str, colour: tuple, anti_ailiasing: bool, x, y, is_centered: bool, scale) -> None:
        super().__init__()

        self.font_path = font_path
        self.font_size = font_size
        self.anti_aliasing = anti_ailiasing
        self.blit_layer = blit_layer
        self.content = content

        if scale != None:
            self.scale = scale
        else: self.scale = 1

        self.font = pygame.font.Font(self.font_path, self.font_size * self.scale)

        self.update(content = content, colour = colour, is_centered = is_centered, x = x, y = y, scale = scale)

  
    def update(self, blit_layer = None, content = None, colour = None, is_centered = None, x = None, y = None, scale = None):
        if blit_layer != None: self.blit_layer = blit_layer
        if content != None: self.content = content
        if colour != None: self.colour = colour
        if is_centered != None: self.is_centered = is_centered
        if x != None: self.x = x
        if y != None: self.y = y
        if scale != None:
            self.scale = scale
            self.font = pygame.font.Font(self.font_path, self.font_size * self.scale)

        self.image = self.font.render(self.content, self.anti_aliasing, self.colour)

        if self.is_centered:
            self.rect = self.image.get_rect(center = (self.x * self.scale, self.y * self.scale))
        else:
            self.rect = self.image.get_rect(topleft = (self.x * self.scale, self.y * self.scale))
    
        self.blit_layer.blit(self.font.render(self.content, self.anti_aliasing, self.colour), self.rect)
