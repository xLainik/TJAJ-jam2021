import pygame, os, random
import queue

from scr.utility.bfs_pathfinding import findEnd, valid

from scr.utility.useful import center_distance, point_distance

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
    def __init__(self, image, x, y, img_offset, entity_name, dialogs, spawn, radius, offset, max_trail, speed, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.dialogs = dialogs

        self.speed = speed

        self.flip = flip

        self.spawn_turn = spawn

        self.active = False

        self.rect = pygame.Rect(x + offset[0], y + offset[1], 20, 20)
        self.x, self.y = float(self.rect.x), float(self.rect.y)

        self.player_state = "never"

        self.player_pos = []
        self.last_player_pos = self.rect.center
        self.directions = []

        self.max_trail = max_trail

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = self.x + offset[0], self.y + offset[1]

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

        self.maze = []
        self.move = False

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
                    start_y, start_x = (entity.rect.y - border_y[0])//20, (entity.rect.x - border_x[0])//20
                elif entity.entity_name == "player":
                    self.maze[round((entity.rect.y - border_y[0])/20)][round((entity.rect.x - border_x[0])/20)] = "X"
                else: self.maze[round((entity.rect.y - border_y[0])/20)][round((entity.rect.x - border_x[0])/20)] = "#"

    def select_move(self, entities, player_rect):

        moves = [True, True, True, True] # right, left, down, up

        # Player is right
        if self.rect.left < player_rect.left - 5:
            moves[1] = False
        elif self.rect.left > player_rect.left - 5:
            moves[0] = False
        elif len(self.directions) > 0:
            for direction in reversed(self.directions):
                moves[0] = not(direction == "L")
                moves[1] = not(direction == "R")
        

        # Player is down
        if self.rect.top < player_rect.top - 5:
            moves[3] = False
        elif self.rect.top > player_rect.top - 5:
            moves[2] = False
        elif len(self.directions) > 0:
            for direction in reversed(self.directions):
                moves[2] = not(direction == "U")
                moves[3] = not(direction == "D")

        for entity in entities:
            if not(entity is self) and entity.entity_name != "player":
                if (entity.rect.centerx in range(self.rect.centerx - 30, self.rect.centerx + 31)) and (entity.rect.centery in range(self.rect.centery - 30, self.rect.centery + 31)):
                    # blocking is on left
                    if entity.rect.collidepoint((self.rect.centerx - 20, self.rect.centery)):
                        moves[1] = False
                    # blocking is on right
                    elif entity.rect.collidepoint((self.rect.centerx + 20, self.rect.centery)):
                        moves[0] = False
                    # blocking is on top
                    elif entity.rect.collidepoint((self.rect.centerx, self.rect.centery - 20)):
                        moves[3] = False
                    # blocking is on bottom
                    elif entity.rect.collidepoint((self.rect.centerx, self.rect.centery + 20)):
                        moves[2] = False

        right_dist, left_dist, down_dist, up_dist = 10000, 10000, 10000, 10000
        
        if moves[0]:
            right_dist = point_distance(player_rect.center, (self.rect.centerx + 20, self.rect.centery))
        if moves[1]:
            left_dist = point_distance(player_rect.center, (self.rect.centerx - 20, self.rect.centery))
        if moves[2]:
            down_dist = point_distance(player_rect.center, (self.rect.centerx, self.rect.centery + 20))
        if moves[3]:
            up_dist = point_distance(player_rect.center, (self.rect.centerx, self.rect.centery - 20))

        distances = [right_dist, left_dist, down_dist, up_dist]

        distances.sort()

        if moves[0] and distances[0] == right_dist:
            return "R"
        elif moves[1] and distances[0] == left_dist:
            return "L"
        elif moves[2] and distances[0] == down_dist:
            return "D"
        elif moves[3] and distances[0] == up_dist:
            return "U"

        return False
                
    def enter_turn(self, entities, player_rect):
        if self.active:
            
            self.circle_color = colours["light gray"]
            self.move = False

            self.player_pos.append((player_rect.centerx, player_rect.centery))
            if len(self.player_pos) > self.max_trail:
                self.player_pos.pop(0)
            
            # Check obstacles that can block vision towards the player
            if center_distance(self.rect, player_rect) <= self.circle_radius:
                # Create the rectangular area between player and guard
                border_x = min(self.rect.left, player_rect.left - 5), max(self.rect.right, player_rect.right + 5)
                border_y = min(self.rect.top, player_rect.top - 5), max(self.rect.bottom, player_rect.bottom + 5)

                self.player_state = "chase"

                self.last_player_pos = player_rect.center

                for entity in entities:
                    if not(entity is self) and entity.entity_name != "player":
                        if entity.rect.centerx in range(border_x[0], border_x[1] + 1) and entity.rect.centery in range(border_y[0], border_y[1] + 1):
                            if len(self.player_pos) > 1:
                                if entity.rect.clipline(self.rect.center, self.player_pos[0]) != () and entity.rect.clipline(self.rect.center, self.player_pos[-1]) != ():
                                    self.player_state = "hidden"
                                    break
                            else:
                                if entity.rect.clipline(self.rect.center, player_rect.center) != ():
                                    self.player_state = "hidden"
                                    break
            else:
                self.player_state = "outside"
                self.player_pos = []
                self.directions = []
            
            if self.player_state == "chase":
                self.move = self.select_move(entities, player_rect)

                self.directions.append(self.move)
                if len(self.directions) > self.max_trail:
                    self.directions.pop(0)

                self.current_ani = self.animations[1]
                self.circle_color = colours["red"]
                
                if self.move == "R":
                    self.flip = False
                    self.speed_x = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif self.move == "L":
                    self.flip = True
                    self.speed_x = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif self.move == "D":
                    self.speed_y = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif self.move == "U":
                    self.speed_y = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20
            else:
                self.current_ani = self.animations[0]
                if self.player_state == "hidden":
                    self.circle_color = colours["green"]
                    self.player_pos = []
                    self.directions = []

        else:
            self.player_pos.append((player_rect.centerx, player_rect.centery))
            if len(self.player_pos) > self.max_trail:
                self.player_pos.pop(0)

    def update(self, entities, delta_time):
        if self.move != False:
            
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
            pygame.draw.circle(layer, self.circle_color, self.rect.center, self.circle_radius, width = 3)
            if self.player_state != "outside" and self.player_state != "never":
                if len(self.player_pos) > 1:
                    if point_distance(self.rect.center, self.player_pos[-1]) >= point_distance(self.player_pos[0], self.player_pos[-1]):
                        pygame.draw.line(layer, colours["yellow"], self.rect.center, self.player_pos[0], width=2)
                        pygame.draw.line(layer, colours["yellow"], self.player_pos[0], self.player_pos[-1], width=2)
                    else:
                        pygame.draw.line(layer, self.circle_color, self.rect.center, self.player_pos[-1], width=2)
                else:
                    pygame.draw.line(layer, self.circle_color, self.rect.center, self.last_player_pos, width=2)

            layer.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 2, self.rect.y - 10))

class Waiter(Obstacle):
    def __init__(self, image, x, y, img_offset, entity_name, orientation, direction, speed, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.orientation = orientation

        self.speed = speed

        self.flip = flip

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
                self.flip = True
                self.speed_x, self.speed_y = -self.speed, 0
                self.move_destination = self.move_destination[0] - 20, self.move_destination[1]
            if self.direction == "R":
                self.flip = False
                self.speed_x, self.speed_y = self.speed, 0
                self.move_destination = self.move_destination[0] + 20, self.move_destination[1]
        else:
            if self.direction == "U":
                self.flip = False
                self.speed_x, self.speed_y = 0, -self.speed
                self.move_destination = self.move_destination[0], self.move_destination[1] - 20
            if self.direction == "D":
                self.flip = True
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
                if not(entity is self):
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
                if not(entity is self):
                    if self.speed_y > 0:
                        self.rect.bottom = entity.rect.top
                        self.collision_directions["bottom"] = True
                    elif self.speed_y < 0:
                        self.rect.top = entity.rect.bottom
                        self.collision_directions["top"] = True
                    self.y = self.rect.y

        if self.orientation == "horizontal":
            if self.collision_directions["left"] or self.collision_directions["right"]:
                if abs(self.rect.x - self.move_destination[0]) > 8:
                    self.speed_x *= -1
                    if self.direction == "L": self.direction = "R"
                    else: self.direction = "L"
                self.move_destination = (round(self.rect.x/20) * 20), self.rect.y

        if self.orientation == "vertical":    
            if self.collision_directions["top"] or self.collision_directions["bottom"]:
                if abs(self.rect.y - self.move_destination[1]) > 8:
                    self.speed_y *= -1
                    if self.direction == "D": self.direction = "U"
                    else: self.direction = "D"
                self.move_destination = self.rect.x, (round(self.rect.y/20) * 20)
                
    
    def draw(self, layer):
        layer.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 4, self.rect.y - 11))

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
            layer.blit(self.popup, (self.rect.x-12, self.rect.y-50))

    def check_action(self, player_rect):
        if center_distance(self.rect, player_rect) < self.action_radius:
            self.popup_active = True
        else: self.popup_active = False

class NPC_1(NPC): # Tecla de reiniciar nivel
    def __init__(self, image, x, y, img_offset, entity_name, offset, action_radius):
        super().__init__(image, x, y, img_offset, entity_name)

        self.action_radius = action_radius

        self.popup = pygame.image.load(os.path.join("scr", "assets", "images", "burbuja 1.png")).convert()

        self.popup_active = False
        
        self.rect = pygame.Rect(x + offset[0], y + offset[0], 20, 20)

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def draw(self, layer):
##        pygame.draw.circle(layer, colours["cyan"], self.rect.center, self.action_radius, width = 3)
        if self.popup_active:
            layer.blit(self.popup, (self.rect.x-40, self.rect.y-52))

    def check_action(self, player_rect):
        if center_distance(self.rect, player_rect) < self.action_radius:
            self.popup_active = True
        else: self.popup_active = False

class NPC_2(NPC): # Camarero Juan, Emma, Oscar
    def __init__(self, image, x, y, img_offset, entity_name, dialogs, action_radius, offset, flip):
        super().__init__(image, x, y, img_offset, entity_name)

        self.flip = flip

        self.action_radius = action_radius

        self.img_offset = img_offset

        self.popup = pygame.image.load(os.path.join("scr", "assets", "images", "burbuja 2.png")).convert()

        self.current_dialog = 0

        self.popup_active = False
        
        self.dialogs = dialogs
        
        self.rect = pygame.Rect(x + offset[0], y + offset[1], 20, 20)

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def enter_turn(self, entities, player_rect):
        if (self.current_dialog < len(self.dialogs) - 1) and self.dialogs[self.current_dialog].already_played:
                self.current_dialog += 1

    def check_action(self, player_rect):
        if center_distance(self.rect, player_rect) < self.action_radius:
            self.dialogs[self.current_dialog].active = True
            self.popup_active = True
            
        else:
            self.dialogs[self.current_dialog].active = False
            self.popup_active = False

    def draw(self, layer):
        layer.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x+self.img_offset[0], self.rect.y+self.img_offset[1]))
##        pygame.draw.circle(layer, colours["cyan"], self.rect.center, self.action_radius, width = 3)??
        if self.popup_active:
            layer.blit(self.popup, (self.rect.x-22, self.rect.y - 50))
