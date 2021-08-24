import pygame

from scr.utility.bfs_pathfinding import findEnd, valid

class Guard(pygame.sprite.Sprite):
    def __init__(self, image, x, y, entity_name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.x, self.y = self.rect.x, self.rect.y

        self.collided, self.moving = False, False
        
        self.entity_name = entity_name

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def create_maze(self, entities, player_rect):
        start_x, end_x = self.rect.x//20, player_rect.x//20
        start_y, end_y = self.rect.y//20, player_rect.y//20

        maze = []
        rows = [" "] * (1 + abs(end_x - start_x))
        for i in range(abs(end_y - start_y) + 1):
            maze.append(rows)

        border_x = min(self.rect.x, player_rect.x), max(self.rect.x, player_rect.x)
        border_y = min(self.rect.y, player_rect.y), max(self.rect.y, player_rect.y)
                
        for entity in entities:
            if entity.rect.x in range(border_x[0], border_x[1] + 1) and entity.rect.y in range(border_y[0], border_y[1] + 1):
                if entity is self:
                    maze[(entity.rect.y - border_x[1])//20][(entity.rect.x - border_x[0])//20] = "0"
                elif entity.entity_name == "player":
                    maze[(entity.rect.y - border_x[1])//20][(entity.rect.x - border_x[0])//20] = "X"
                else: maze[(entity.rect.y - border_x[1])//20][(entity.rect.x - border_x[0])//20] = "#"

        print(maze)

    def update(self, entities, player_turn, player_rect, delta_time):
##        self.create_maze(entities, player_rect)
        pass
    
    def draw(self, layer):
        layer.blit(self.image, self.rect)
