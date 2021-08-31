import pygame, os, random
import queue

from scr.utility.bfs_pathfinding import findEnd, valid

from scr.utility.useful import center_distance

from scr.config.config import colours

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, img_offset, entity_name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 20, 20)
        
        self.x, self.y = self.rect.x, self.rect.y

        self.img_offset = img_offset

        self.flip = False

        self.collided, self.moving = False, False

        self.push_directions = {"left": True, "right": True, "down": True, "up": True}

        self.entity_name = entity_name

        if type(image) == list:
            # [{ani_1}, {ani_2}, etc]
            self.animations = image
            self.current_ani = self.animations[0]
            self.image = self.current_ani["0"]
        else:
            # single img to blit (no animation)
            self.image = image
            self.animations = None
            

    def on_collide(self):
        pass

    def on_action(self):
        pass

    def check_action(self, player_rect):
        pass
    
    def enter_turn(self, entities, player_rect):
        pass
    
    def update(self, entities, delta_time):
        pass
    
    def draw(self, layer):
        layer.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x + self.img_offset[0], self.rect.y + self.img_offset[1]))

    def change_frame(self, current_beat):
        for key, frame in self.current_ani.items():
            if int(key) == current_beat:
                self.image = frame

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
    def __init__(self, image, x, y, img_offset, entity_name):
        super().__init__(image, x, y, img_offset, entity_name)
        
        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

class Goal(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, game):
        super().__init__(image, x, y, img_offset, entity_name)

        self.game = game
        
        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def on_collide(self):
        self.game.current_level += 1
        self.game.player.dead = True

class Table(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, speed):
        super().__init__(image, x, y, img_offset, entity_name)

        self.speed = speed
        
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
                        self.speed_x = self.speed
                        self.moving = True
                        self.move_destination = self.rect.x + 20, self.rect.y
                    elif self.push_directions["left"] and entity.speed_x < 0:
                        self.speed_x = -self.speed
                        self.moving = True
                        self.move_destination = self.rect.x - 20, self.rect.y
                    elif self.push_directions["down"] and entity.speed_y > 0:
                        self.speed_y = self.speed
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y + 20
                    elif self.push_directions["up"] and entity.speed_y < 0:
                        self.speed_y = -self.speed
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y - 20
        

class Box(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, speed):
        super().__init__(image, x, y, img_offset, entity_name)

        self.speed = speed

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
                    self.speed_x = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif self.push_directions["left"] and entity.speed_x < 0:
                    self.speed_x = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif self.push_directions["down"] and entity.speed_y > 0:
                    self.speed_y = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif self.push_directions["up"] and entity.speed_y < 0:
                    self.speed_y = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x, self.rect.y))

class Guard(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, dialogs, spawn, radius, offset, speed, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.dialogs = dialogs

        self.speed = speed

        self.spawn_turn = spawn

        self.active = False

        self.rect = pygame.Rect(x + offset[0], y + offset[1], 20, 20)
        self.x, self.y = float(self.rect.x), float(self.rect.y)

        self.direction = "R"

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x + offset[0], self.y + offset[1]

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
                    self.maze[round((entity.rect.y - border_y[0])/20)][round((entity.rect.x - border_x[0])/20)] = "X"
                else: self.maze[round((entity.rect.y - border_y[0])/20)][round((entity.rect.x - border_x[0])/20)] = "#"

    def enter_turn(self, entities, player_rect):
        if self.active:
            
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
                self.current_ani = self.animations[0]
                if moves == False:
                    self.circle_color = colours["green"]
                self.moves = False
            else:
                self.current_ani = self.animations[1]
                self.moves = tuple(moves)

                self.direction = moves[0]

                self.circle_color = colours["red"]
                
                if self.moves[0] == "R":
                    self.speed_x = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif self.moves[0] == "L":
                    self.speed_x = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif self.moves[0] == "D":
                    self.speed_y = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif self.moves[0] == "U":
                    self.speed_y = -self.speed
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

    def on_collide(self):
        if self.active:
            rand_int = random.randint(0, len(self.dialogs) - 1)
            self.dialogs[rand_int].must_action = False
            self.dialogs[rand_int].active = True
               
    def draw(self, layer):
        if self.active:
            layer.blit(self.image, self.rect)
            pygame.draw.circle(layer, self.circle_color, self.rect.center, self.circle_radius, width = 3)

class Waiter(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, orientation, direction, speed, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.orientation = orientation

        self.speed = speed

        self.active = False

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        
        self.moving = False
        self.move_destination = self.x, self.y

        if direction == "izquierda":
            self.direction = "L"
            self.speed_x, self.speed_y = -self.speed, 0
        if direction == "derecha":
            self.direction = "R"
            self.speed_x, self.speed_y = self.speed, 0
        if direction == "arriba":
            self.direction = "U"
            self.speed_x, self.speed_y = 0, -self.speed
        if direction == "abajo":
            self.direction = "D"
            self.speed_x, self.speed_y = 0, self.speed

    def enter_turn(self, entities, player_rect):
        self.moving = True

##        print((self.rect.x, self.rect.y), self.move_destination)

        if self.orientation == "horizontal":
            if self.direction == "L":
                self.speed_x, self.speed_y = -self.speed, 0
                self.move_destination = self.move_destination[0] - 20, self.move_destination[1]
            if self.direction == "R":
                self.speed_x, self.speed_y = self.speed, 0
                self.move_destination = self.move_destination[0] + 20, self.move_destination[1]
        else:
            if self.direction == "U":
                self.speed_x, self.speed_y = 0, -self.speed
                self.move_destination = self.move_destination[0], self.move_destination[1] - 20
            if self.direction == "D":
                self.speed_x, self.speed_y = 0, self.speed
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
                self.active = False
                
        if self.active:
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
    def __init__(self, image, x, y, img_offset, entity_name):
        super().__init__(image, x, y, img_offset, entity_name)

    def draw(self, layer):
        layer.blit(self.image, self.rect)
        pygame.draw.circle(layer, colours["cyan"], self.rect.center, self.action_radius, width = 3)

class NPC_0(NPC): # Controles de moverse
    def __init__(self, image, x, y, img_offset, entity_name, offset, action_radius):
        super().__init__(image, x, y, img_offset, entity_name)

        self.action_radius = action_radius

        self.popup = pygame.image.load(os.path.join("scr", "assets", "images", "burbuja 0.png")).convert()

        self.popup_active = False
        
        self.rect = pygame.Rect(x + offset[0], y + offset[0], 20, 20)

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def draw(self, layer):
##        pygame.draw.circle(layer, colours["cyan"], self.rect.center, self.action_radius, width = 3)
        if self.popup_active:
            layer.blit(self.popup, (self.rect.x-2, self.rect.y-24))

    def check_action(self, player_rect):
        if center_distance(self.rect, player_rect) < self.action_radius:
            self.popup_active = True
        else: self.popup_active = False

class NPC_2(NPC): # Camarero echando carro
    def __init__(self, image, x, y, img_offset, entity_name, dialogs, action_radius, offset, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.flip = flip

        self.action_radius = action_radius

        self.dialogs = dialogs
        
        self.rect = pygame.Rect(x + offset[0], y + offset[1], 20, 20)

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def check_action(self, player_rect):
        if center_distance(self.rect, player_rect) < self.action_radius:
            self.dialogs[0].active = True
        else:
            self.dialogs[0].active = False

    def draw(self, layer):
        layer.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.circle(layer, colours["cyan"], self.rect.center, self.action_radius, width = 3)
