import pygame, os

from scr.utility.bfs_pathfinding import findEnd, valid
import queue

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, entity_name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.x, self.y = self.rect.x, self.rect.y

        self.collided, self.moving = False, False

        self.push_directions = {"left": True, "right": True, "down": True, "up": True}

        self.entity_name = entity_name

    def enter_turn(self, entities, player_rect):
        pass
    
    def update(self, entities, delta_time):
        pass
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x, self.rect.y))

    def calculate_push(self, entities):

        self.push_directions = {"left": True, "right": True, "down": True, "up": True}
        
        for entity in entities:
            if not(entity is self):
                if (entity.rect.centerx in range(self.rect.centerx - 30, self.rect.centerx + 31)) and (entity.rect.centery in range(self.rect.centery - 30, self.rect.centery + 31)):
                    # blocking is on left
                    if entity.rect.collidepoint((self.rect.centerx - 20, self.rect.centery)):
                        self.push_directions["left"] = False
                    # blocking is on right
                    if entity.rect.collidepoint((self.rect.centerx + 20, self.rect.centery)):
                        self.push_directions["right"] = False
                    # blocking is on top
                    if entity.rect.collidepoint((self.rect.centerx, self.rect.centery - 20)):
                        self.push_directions["up"] = False
                    # blocking is on bottom
                    if entity.rect.collidepoint((self.rect.centerx, self.rect.centery + 20)):
                        self.push_directions["down"] = False

class Barrier(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)
        
        self.rect = pygame.Rect(x, y, 20, 20)
        
        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def update(self, entities, delta_time):
        pass

class Table(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x, self.y

        self.down_image = pygame.image.load(os.path.join("scr", "assets", "images", "mesa caida.png"))

        self.standing = True

    def update(self, entities, delta_time):

        print(self.standing, self.moving, self.push_directions)

        if self.standing:
            self.calculate_push(entities)
        
        # grid movement
        if self.moving and self.standing:
            if self.speed_x > 0:
                if self.rect.x >= self.move_destination[0]:
                    self.moving = False
            elif self.speed_x < 0:
                if self.rect.x <= self.move_destination[0]:
                    self.moving = False
            elif self.speed_y > 0:
                if self.rect.y >= self.move_destination[1]:
                    self.moving = False
            elif self.speed_y < 0:
                if self.rect.y <= self.move_destination[1]:
                    self.moving = False
                
            if self.moving == False:
                self.speed_x, self.speed_y = 0, 0
                self.x, self.y = self.move_destination
                self.standing = False
                self.push_directions = {"left": False, "right": False, "down": False, "up": False}

        if self.standing:
            # Applies the speed to the position
            self.x += self.speed_x * delta_time
            self.y += self.speed_y * delta_time

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            hit_list = pygame.sprite.spritecollide(self, entities, False)

            for entity in hit_list:
                # The player pushed the obstacle
                if entity.entity_name == "player" and not(entity is self):
                    if self.push_directions["right"] and entity.speed_x > 0:
                        self.speed_x = 3
                        self.moving = True
                        self.move_destination = self.rect.x + 20, self.rect.y
                    elif self.push_directions["left"] and entity.speed_x < 0:
                        self.speed_x = -3
                        self.moving = True
                        self.move_destination = self.rect.x - 20, self.rect.y
                    elif self.push_directions["down"] and entity.speed_y > 0:
                        self.speed_y = 3
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y + 20
                    elif self.push_directions["up"] and entity.speed_y < 0:
                        self.speed_y = -3
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y - 20
                    self.image = self.down_image
        

class Box(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.rect = pygame.Rect(x, y, 20, 20)
        self.x, self.y = self.rect.x, self.rect.y

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x, self.y

    def update(self, entities, delta_time):

        self.calculate_push(entities)
        
        # grid movement
        if self.moving:
            if self.speed_x > 0:
                if self.rect.x >= self.move_destination[0]:
                    self.moving = False
            elif self.speed_x < 0:
                if self.rect.x <= self.move_destination[0]:
                    self.moving = False
            elif self.speed_y > 0:
                if self.rect.y >= self.move_destination[1]:
                    self.moving = False
            elif self.speed_y < 0:
                if self.rect.y <= self.move_destination[1]:
                    self.moving = False
                
            if self.moving == False:
                self.speed_x, self.speed_y = 0, 0
                self.x, self.y = self.move_destination
                
        # Applies the speed to the position
        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        hit_list = pygame.sprite.spritecollide(self, entities, False)

        for entity in hit_list:
            # The player pushed the obstacle
            if entity.entity_name == "player" and not(self.moving):
                if self.push_directions["right"] and entity.speed_x > 0:
                    self.speed_x = 3
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif self.push_directions["left"] and entity.speed_x < 0:
                    self.speed_x = -3
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif self.push_directions["down"] and entity.speed_y > 0:
                    self.speed_y = 3
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif self.push_directions["up"] and entity.speed_y < 0:
                    self.speed_y = -3
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x, self.rect.y))

class Guard(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.blue_image = pygame.image.load(os.path.join("scr", "assets", "images", "guardia azul.png"))
        self.red_image = pygame.image.load(os.path.join("scr", "assets", "images", "guardia.png"))

        self.image = self.blue_image

        self.rect = pygame.Rect(x, y, 20, 20)

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x, self.y

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

        self.maze = []
        self.moves = False

    def create_maze(self, entities, player_rect):
        start_x, end_x = self.rect.x//20, player_rect.x//20
        start_y, end_y = self.rect.y//20, player_rect.y//20

        self.maze = [[" " for i in range(abs(end_x - start_x) + 1)] for j in range(abs(end_y - start_y) + 1)]

        border_x = min(self.rect.left, player_rect.left - 5), max(self.rect.right, player_rect.right + 5)
        border_y = min(self.rect.top, player_rect.top - 5), max(self.rect.bottom, player_rect.bottom + 5)
                
        for entity in entities:
            if entity.rect.centerx in range(border_x[0], border_x[1] + 1) and entity.rect.centery in range(border_y[0], border_y[1] + 1):
                if entity is self:
                    self.maze[(entity.rect.y - border_y[0])//20][(entity.rect.x - border_x[0])//20] = "O"
                    self.start_y, self.start_x = (entity.rect.y - border_y[0])//20, (entity.rect.x - border_x[0])//20
##                    print(self.start_x, self.start_y)
                elif entity.entity_name == "player":
                    self.maze[(entity.rect.y - border_y[0])//20][(entity.rect.x - border_x[0])//20] = "X"
                else: self.maze[(entity.rect.y - border_y[0])//20][(entity.rect.x - border_x[0])//20] = "#"

    def enter_turn(self, entities, player_rect):
        self.create_maze(entities, player_rect)
        print(self.maze)

        nums = queue.Queue()
        nums.put("")
        add = ""
        moves = False

        timer = 0
        while timer < 100:
            moves = findEnd(self.maze, add, self.start_x, self.start_y)
            if moves != False: timer = 100
            add = nums.get()
            for j in ["L", "R", "U", "D"]:
                put = add + j
                if valid(self.maze, put, self.start_x, self.start_y):
                    nums.put(put)
            timer += 1
            
        print(moves)
            
        if moves == False:
            self.image = self.blue_image
            self.moves = False
        else:
            self.image = self.red_image
            self.moves = tuple(moves)
            
            if self.moves[0] == "R":
                self.speed_x = 3
                self.moving = True
                self.move_destination = self.rect.x + 20, self.rect.y
            elif self.moves[0] == "L":
                self.speed_x = -3
                self.moving = True
                self.move_destination = self.rect.x - 20, self.rect.y
            elif self.moves[0] == "D":
                self.speed_y = 3
                self.moving = True
                self.move_destination = self.rect.x, self.rect.y + 20
            elif self.moves[0] == "U":
                self.speed_y = -3
                self.moving = True
                self.move_destination = self.rect.x, self.rect.y - 20

    def update(self, entities, delta_time):
        if self.moves != False:
            # grid movement
            if self.moving:
                if self.speed_x > 0:
                    if self.rect.x >= self.move_destination[0]:
                        self.moving = False
                elif self.speed_x < 0:
                    if self.rect.x <= self.move_destination[0]:
                        self.moving = False
                elif self.speed_y > 0:
                    if self.rect.y >= self.move_destination[1]:
                        self.moving = False
                elif self.speed_y < 0:
                    if self.rect.y <= self.move_destination[1]:
                        self.moving = False
                    
                if self.moving == False:
                    self.speed_x, self.speed_y = 0, 0
                    self.x, self.y = self.move_destination
                    
            # Applies the speed to the position
            self.x += self.speed_x
            self.y += self.speed_y

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
   
               
    def draw(self, layer):
        layer.blit(self.image, self.rect)
