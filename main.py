import pygame, os

def loadImage(image_path, size = None):
    if size != None:
        return pygame.transform.scale(pygame.image.load(image_path).convert(), size)
    return pygame.image.load(image_path)

if __name__ == "__main__":
    from scr.game import Game
    game = Game()
    while game.running:
        game.new()
