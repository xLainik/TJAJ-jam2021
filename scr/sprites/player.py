import pygame
from scr.config.config import colours

from scr.utility.easying import easeInOutExpo

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(colours["green"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0

        self.game = game

        self.speed = 0

        self.miss_beat = False

        self.entity_name = "player"

        self.restart_cooldown = 0

        self.dead = False
        self.moving = False
        self.move_destination = 0, 0

        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}        
        self.inputs = {"right": False, "left": False, "up": False, "down": False, "space": False, "restart": False}

    def level_init(self, x, y, speed):
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0
        self.move_destination = x, y

        self.speed = speed

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
                    self.move_destination = self.rect.x + 20, self.rect.y
                    self.inputs["right"] = True
                    self.can_move = False
            elif self.game.actions["left"] and not(self.miss_beat):
                if not(player_turn):
                    self.miss_beat = True
                elif self.can_move:
                    self.speed_x = -self.speed
                    self.moving = True
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

##        self.inputs["restart"] = self.game.actions["r"]
##        
##        if not(self.dead) and self.can_move:
##            if self.game.actions["right"]:
##                self.speed_x = self.speed
##                self.moving = True
##                self.move_destination = self.rect.x + 20, self.rect.y
##                self.inputs["right"] = True
##                self.can_move = False
##            elif self.game.actions["left"]:
##                self.speed_x = -self.speed
##                self.moving = True
##                self.move_destination = self.rect.x - 20, self.rect.y
##                self.inputs["left"] = True
##                self.can_move = False
##            elif self.game.actions["down"]:
##                self.speed_y = self.speed
##                self.moving = True
##                self.move_destination = self.rect.x, self.rect.y + 20
##                self.inputs["down"] = True
##                self.can_move = False
##            elif self.game.actions["up"]:
##                self.speed_y = -self.speed
##                self.moving = True
##                self.move_destination = self.rect.x, self.rect.y - 20
##                self.inputs["up"] = True
##                self.can_move = False

        

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

    def change_animation(self, new_ani):
        if self.current_ani != new_ani:
            self.previous_ani = self.current_ani
            self.ani_timer = 0
            self.ani_frame = 0
            self.current_ani = new_ani

    def draw(self, layer):

##        if self.current_ani[0][0][1] == 0: # no animation
##            layer.blit(pygame.transform.flip(self.current_ani[0][0][0], self.flip, False), (self.rect.x-self.current_ani[2][0],self.rect.y-self.current_ani[2][1]))
##        else:
##            layer.blit(pygame.transform.flip(self.current_ani[0][self.ani_frame][0], self.flip, False), (self.rect.x-self.current_ani[2][0],self.rect.y-self.current_ani[2][1]))
##            if self.ani_timer < self.current_ani[0][self.ani_frame][1]:
##                self.ani_timer += self.game.delta_time
##            else:
##                self.ani_timer = 0
##                self.ani_frame += 1
##            if self.ani_frame >= len(self.current_ani[0]):
##                if self.current_ani[1] == True:
##                    self.ani_timer, self.ani_frame = 0, 0
##                else: self.change_animation(self.previous_ani)
        
        pygame.draw.rect(layer, colours["red"], self.rect)
##        pygame.draw.rect(layer, (0, 255, 0), (self.move_destination[0], self.move_destination[1], 10, 10))
