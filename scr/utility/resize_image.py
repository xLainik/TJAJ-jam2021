import pygame

def resize(surface, game_scale, image_scale):

    scale = game_scale/image_scale    
    
    image = pygame.transform.smoothscale(surface.convert_alpha(), (int(surface.get_width() * scale), int(surface.get_height() * scale)))
##    image_copy = pygame.Surface(image.get_size())
##    image_copy.set_colorkey((0,0,0))
##    image_copy.fill((0,0,0))
##    image_copy.blit(image, (0,0))
    
##    pygame.image.save(image, "prueba.png")
    return image
