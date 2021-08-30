import pygame
from scr.config.config import colours

from scr.utility.easying import easeInOutExpo

class Player(pygame.sprite.Sprite):
    def __init__(self, game, image, x , y, img_offset):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((x + 5, y + 5, 10, 10))
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0

        self.game = game

        self.img_offset = img_offset

        self.animations = image
        self.current_ani = self.animations[0]
        self.image = self.current_ani["0"]

        self.flip = False

        self.speed = 0

        self.miss_beat = False

        self.entity_name = "player"

        self.restart_cooldown = 0

        self.dead = False
        self.moving = False
        self.move_destination = 0, 0

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}        
        self.inputs = {"right": False, "left": False, "up": False, "down": False, "space": False, "restart": False}

    def level_init(self, x, y, speed, flip):
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0
        self.move_destination = x, y

        self.speed = speed

        self.flip = flip

        self.dead = False
        self.moving = False
        self.move_destination = 0, 0

        self.can_move = True
        
        self.restart_cooldown = 0

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        self.inputs = {"right": False, "left": False, "up": False, "down": False, "skip": False, "restart": False}
        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def enter_turn(self, entities, player_rect):
        pass

    def check_inputs(self, player_turn):
        self.inputs["restart"] = self.game.actions["r"]
        
        if not(self.dead):
            if self.game.actions["right"] and not(self.miss_beat):
                if not(player_turn):
                    self.miss_beat = True
                elif self.can_move:
                    self.speed_x = self.speed
                    self.moving = True
                    self.flip = False
                    self.move_destination = self.rect.x + 20, self.rect.y
                    self.inputs["right"] = True
                    self.can_move = False
            elif self.game.actions["left"] and not(self.miss_beat):
                if not(player_turn):
                    self.miss_beat = True
                elif self.can_move:
                    self.speed_x = -self.speed
                    self.moving = True
                    self.flip = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                    self.inputs["left"] = True
                    self.can_move = False
            elif self.game.actions["down"] and not(self.miss_beat):
                if not(player_turn):
                    self.miss_beat = True
                elif self.can_move:
                    self.speed_y = self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                    self.inputs["down"] = True
                    self.can_move = False
            elif self.game.actions["up"] and not(self.miss_beat):
                if not(player_turn):
                    self.miss_beat = True
                elif self.can_move:
                    self.speed_y = -self.speed
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20
                    self.inputs["up"] = True
                    self.can_move = False

            # Restart the level
        if self.inputs["restart"] and self.restart_cooldown == -1:
            self.game.transition_timer = 0
            self.restart_cooldown = 0
                
        if self.game.transition_timer >= 26:
            self.dead = True

        if self.restart_cooldown >= 0:
            self.restart_cooldown += self.game.delta_time
            if self.restart_cooldown >= 100: self.restart_cooldown = -1
        
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
                self.inputs = {"right": False, "left": False, "up": False, "down": False, "space": False, "restart": False}
                self.speed_x, self.speed_y = 0, 0
                self.x, self.y = self.move_destination
                
        # Applies the speed to the position
        self.x += self.speed_x * self.game.delta_time
        self.y += self.speed_y * self.game.delta_time

        # Collision direction from the player reference point
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)

        hit_list_1 = pygame.sprite.spritecollide(self, entities, False)

        for entity in hit_list_1:
            if not(entity is self):
                entity.on_collide()
                if entity.entity_name != "guardia":
                    if (entity.push_directions["right"] == False) and self.speed_x > 0:
                        self.rect.right = entity.rect.left
                        self.collision_directions["right"] = True
                    elif (entity.push_directions["left"] == False) and self.speed_x < 0:
                        self.rect.left = entity.rect.right
                        self.collision_directions["left"] = True
                    self.x = self.rect.x
                elif entity.active: self.dead = True
        self.rect.y = int(self.y)
            
        hit_list_2 = pygame.sprite.spritecollide(self, entities, False)
        
        for entity in hit_list_2:
            if not(entity in hit_list_1) and not(entity is self):
                entity.on_collide()
                if entity.entity_name != "guardia":
                    if (entity.push_directions["down"] == False) and self.speed_y > 0:
                        self.rect.bottom = entity.rect.top
                        self.collision_directions["bottom"] = True
                    elif (entity.push_directions["up"] == False) and self.speed_y < 0:
                        self.rect.top = entity.rect.bottom
                        self.collision_directions["top"] = True
                    self.y = self.rect.y
                elif entity.active: self.dead = True

        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.move_destination = (round(self.rect.x//20) * 20) + 5, self.rect.y
            self.speed_x *= -1
            
        if self.collision_directions["top"] or self.collision_directions["bottom"]:
            self.move_destination = self.rect.x, (round(self.rect.y//20) * 20) + 5
            self.speed_y *= -1

    def draw(self, layer):
        layer.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x + self.img_offset[0], self.rect.y + self.img_offset[1]))
##        pygame.draw.rect(layer, colours["red"], self.rect, width=2)

    def change_frame(self, current_beat):
        for key, frame in self.current_ani.items():
            if int(key) == current_beat:
                self.image = frame
        
