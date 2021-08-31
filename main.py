import pygame, os

if __name__ == "__main__":
    from scr.game import Game
    game = Game()
    while game.running:
        game.new()
