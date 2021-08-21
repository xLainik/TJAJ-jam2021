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

        self.dead = False
        self.moving = False
        self.move_destination = 0, 0
        
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}
        self.inputs = {"right": False, "left": False, "up": False, "down": False}

    def level_init(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.x, self.y = float(x), float(y)
        self.speed_x, self.speed_y = 0, 0
        self.move_destination = x, y

    def check_dead(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and not(self.dead):
                self.dead = True
        
    def update(self, tiles):
        
        if not(self.dead) and not(self.moving):
            if self.game.actions[pygame.K_RIGHT]:
                self.speed_x = 1
                self.moving = True
                self.move_destination = self.rect.x + 20, self.rect.y
                self.inputs["right"] = True
            elif self.game.actions[pygame.K_LEFT]:
                self.speed_x = -1
                self.moving = True
                self.move_destination = self.rect.x - 20, self.rect.y
                self.inputs["left"] = True
            elif self.game.actions[pygame.K_DOWN]:
                self.speed_y = 1
                self.moving = True
                self.move_destination = self.rect.x, self.rect.y + 20
                self.inputs["down"] = True
            elif self.game.actions[pygame.K_UP]:
                self.speed_y = -1
                self.moving = True
                self.move_destination = self.rect.x, self.rect.y - 20
                self.inputs["up"] = True

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
                self.inputs = {"right": False, "left": False, "up": False, "down": False}
                self.speed_x, self.speed_y = 0, 0
                self.x, self.y = self.move_destination
                
        # Applies the speed to the position
        self.x += self.speed_x * self.game.delta_time
        self.y += self.speed_y * self.game.delta_time

        # Collision direction from the player reference point
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)

        hit_list = pygame.sprite.spritecollide(self, tiles, False)

        for tile in hit_list:
            if tile.collidable:
                if self.speed_x > 0:
                    self.rect.right = tile.rect.left
                    self.collision_directions["right"] = True
                elif self.speed_x < 0:
                    self.rect.left = tile.rect.right
                    self.collision_directions["left"] = True
                self.x = self.rect.x

        self.rect.y = int(self.y)
            
        hit_list = pygame.sprite.spritecollide(self, tiles, False)
        
        for tile in hit_list:
            if tile.collidable:
                if self.speed_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.collision_directions["bottom"] = True
                elif self.speed_y < 0 and not(self.dead):
                    self.rect.top = tile.rect.bottom
                    self.collision_directions["top"] = True
                self.y = self.rect.y

        if self.collision_directions["left"] or self.collision_directions["right"]:
            self.move_destination = ((self.rect.x//20) * 20) + 5, self.rect.y
            self.speed_x *= -1
            
        if self.collision_directions["top"] or self.collision_directions["bottom"]:
            self.move_destination = self.rect.x, ((self.rect.y//20) * 20) + 5
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
        pygame.draw.rect(layer, colours["green"], self.rect)