import pygame, os
import queue

from scr.utility.bfs_pathfinding import findEnd, valid

from scr.utility.useful import center_distance

from scr.config.config import colours

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

    def on_collide(self):
        pass

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

                # Obstaculos movibles se transpan
                # WIP
                
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

    def enter_turn(self, entities, player_rect):
        if self.standing:
            self.calculate_push(entities)

    def update(self, entities, delta_time):

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
                self.image = self.down_image
                self.move_destination = self.x, self.y

        if self.standing:
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
                        self.speed_x = 2
                        self.moving = True
                        self.move_destination = self.rect.x + 20, self.rect.y
                    elif self.push_directions["left"] and entity.speed_x < 0:
                        self.speed_x = -2
                        self.moving = True
                        self.move_destination = self.rect.x - 20, self.rect.y
                    elif self.push_directions["down"] and entity.speed_y > 0:
                        self.speed_y = 2
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y + 20
                    elif self.push_directions["up"] and entity.speed_y < 0:
                        self.speed_y = -2
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y - 20
        

class Box(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.rect = pygame.Rect(x, y, 20, 20)
        self.x, self.y = self.rect.x, self.rect.y

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x, self.y

    def enter_turn(self, entities, player_rect):
        self.calculate_push(entities)
        
    def update(self, entities, delta_time):
        
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
    def __init__(self, image, x, y, entity_name, spawn, radius):
        super().__init__(image, x, y, entity_name)

        self.blue_image = pygame.image.load(os.path.join("scr", "assets", "images", "guardia azul.png"))
        self.red_image = pygame.image.load(os.path.join("scr", "assets", "images", "guardia.png"))

        self.image = self.blue_image

        self.spawn_turn = spawn

        self.active = False

        self.rect = pygame.Rect(x, y, 20, 20)

        self.direction = "R"

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x, self.y

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

        self.maze = []
        self.moves = False

        self.circle_color = colours["light gray"]
        self.circle_radius = radius

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
                elif entity.entity_name == "player":
                    self.maze[(entity.rect.y - border_y[0])//20][(entity.rect.x - border_x[0])//20] = "X"
                else: self.maze[(entity.rect.y - border_y[0])//20][(entity.rect.x - border_x[0])//20] = "#"

    def enter_turn(self, entities, player_rect):
        
        self.create_maze(entities, player_rect)

        self.circle_color = colours["light gray"]
        moves = True
        
        if center_distance(self.rect, player_rect) < self.circle_radius:

            if len(self.maze[0]) == 1:
                for tile in self.maze:
                    if tile[0] == "#":
                        moves = False
            elif len(self.maze) == 1:
                for tile in self.maze[0]:
                    if tile == "#":
                        moves = False
            if moves == True:
                nums = queue.Queue()
                nums.put("")
                add = ""
                
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
        if type(moves) == bool or len(moves) == 0:
            self.image = self.blue_image
            if moves == False:
                self.circle_color = colours["green"]
            self.moves = False
        else:
            self.image = self.red_image
            self.moves = tuple(moves)

            self.direction = moves[0]

            self.circle_color = colours["red"]
            
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
        if self.active:
            layer.blit(self.image, self.rect)
            pygame.draw.circle(layer, self.circle_color, self.rect.center, self.circle_radius, width = 3)

class Waiter(Obstacle):
    def __init__(self, image, x, y, entity_name, orientation, direction):
        super().__init__(image, x, y, entity_name)

        self.orientation = orientation
        
        self.rect = pygame.Rect(x, y, 20, 20)
        self.x, self.y = self.rect.x, self.rect.y

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        
        self.moving = False
        self.move_destination = self.x, self.y

        if direction == "izquierda":
            self.direction = "L"
            self.speed_x, self.speed_y = -3, 0
        if direction == "derecha":
            self.direction = "R"
            self.speed_x, self.speed_y = 3, 0
        if direction == "arriba":
            self.direction = "U"
            self.speed_x, self.speed_y = 0, -3
        if direction == "abajo":
            self.direction = "D"
            self.speed_x, self.speed_y = 0, 3

    def enter_turn(self, entities, player_rect):
        self.moving = True

##        print((self.rect.x, self.rect.y), self.move_destination)

        if abs(self.move_destination[0] - self.rect.x) < 10 and abs(self.move_destination[1] - self.rect.y) < 10:
            if self.orientation == "horizontal":
                if self.direction == "L":
                    self.speed_x, self.speed_y = -3, 0
                    self.move_destination = self.move_destination[0] - 20, self.move_destination[1]
                if self.direction == "R":
                    self.speed_x, self.speed_y = 3, 0
                    self.move_destination = self.move_destination[0] + 20, self.move_destination[1]
            else:
                if self.direction == "U":
                    self.speed_x, self.speed_y = 0, -3
                    self.move_destination = self.move_destination[0], self.move_destination[1] - 20
                if self.direction == "D":
                    self.speed_x, self.speed_y = 0, 3
                    self.move_destination = self.move_destination[0], self.move_destination[1] + 20
                
        
        
    def update(self, entities, delta_time):        
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
                self.x, self.y = self.move_destination
                self.speed_x, self.speed_y = 0, 0
                
                
        # Applies the speed to the position
        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        # Collision direction from the player reference point
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)

        if self.orientation == "horizontal":
            hit_list = pygame.sprite.spritecollide(self, entities, False)

            for entity in hit_list:
                if not(entity is self) and entity.entity_name != "player":
                    if self.speed_x > 0:
                        self.rect.right = entity.rect.left
                        self.collision_directions["right"] = True
                    elif self.speed_x < 0:
                        self.rect.left = entity.rect.right
                        self.collision_directions["left"] = True
                    self.x = self.rect.x

        self.rect.y = int(self.y)

        if self.orientation == "vertical":
            hit_list = pygame.sprite.spritecollide(self, entities, False)
            
            for entity in hit_list:
                if not(entity is self) and entity.entity_name != "player":
                    if self.speed_y > 0:
                        self.rect.bottom = entity.rect.top
                        self.collision_directions["bottom"] = True
                    elif self.speed_y < 0:
                        self.rect.top = entity.rect.bottom
                        self.collision_directions["top"] = True
                    self.y = self.rect.y

        if self.orientation == "horizontal":
            if self.collision_directions["left"] or self.collision_directions["right"]:
                self.move_destination = (round(self.rect.x/20) * 20), self.rect.y
                self.speed_x *= -1
                if self.direction == "L": self.direction = "R"
                else: self.direction = "L"

        if self.orientation == "vertical":    
            if self.collision_directions["top"] or self.collision_directions["bottom"]:
                self.move_destination = self.rect.x, (round(self.rect.y/20) * 20)
                self.speed_y *= -1
                if self.direction == "D": self.direction = "U"
                else: self.direction = "D"
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x, self.rect.y))

class NPC(Obstacle):
    def __init__(self, image, x, y, entity_name, dialogs):
        super().__init__(image, x, y, entity_name)

##        print(dialog_list)

        self.dialogs = dialogs
        
        self.rect = pygame.Rect(x, y, 20, 20)
        
        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def update(self, entities, delta_time):
        pass

    def on_collide(self):

        print("START DIALOG")
        
        self.dialogs[0].active = True
