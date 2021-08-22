import pygame, os

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, entity_name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.x, self.y = self.rect.x, self.rect.y

        self.collided, self.moving = False, False

        self.push_directions = {"left": True, "right": True, "bottom": True, "top": True}

        self.entity_name = entity_name

    def update(self, entities, player_turn, delta_time):
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
##                        print("push LEFT blocked")
                    # blocking is on right
                    if entity.rect.collidepoint((self.rect.centerx + 20, self.rect.centery)):
                        self.push_directions["right"] = False
##                        print("push RIGHT blocked")
                    # blocking is on top
                    if entity.rect.collidepoint((self.rect.centerx, self.rect.centery - 20)):
                        self.push_directions["up"] = False
##                        print("push UP blocked")
                    # blocking is on bottom
                    if entity.rect.collidepoint((self.rect.centerx, self.rect.centery + 20)):
                        self.push_directions["down"] = False
##                        print("push DOWN blocked")

class Barrier(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)
        
        self.rect = pygame.Rect(x, y, 20, 20)

        self.push_directions = {"left": False, "right": False, "down": False, "up": False}

    def update(self, entities, player_turn, delta_time):
        pass

class Table(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.standing = True

    def update(self, entities, player_turn, delta_time):

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
                self.image = pygame.image.load(os.path.join("scr", "assets", "images", "mesa caida.png"))
                self.move_destination = -10, -10

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
                        self.speed_x = 1
                        self.moving = True
                        self.move_destination = self.rect.x + 20, self.rect.y
                    elif self.push_directions["left"] and entity.speed_x < 0:
                        self.speed_x = -1
                        self.moving = True
                        self.move_destination = self.rect.x - 20, self.rect.y
                    elif self.push_directions["down"] and entity.speed_y > 0:
                        self.speed_y = 1
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y + 20
                    elif self.push_directions["up"] and entity.speed_y < 0:
                        self.speed_y = -1
                        self.moving = True
                        self.move_destination = self.rect.x, self.rect.y - 20
        

class Box(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.rect = pygame.Rect(x, y, 20, 20)
        self.x, self.y = self.rect.x, self.rect.y

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = -10, -10

    def update(self, entities, player_turn, delta_time):

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
                self.move_destination = -10, -10
                
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
                    self.speed_x = 1
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif self.push_directions["left"] and entity.speed_x < 0:
                    self.speed_x = -1
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif self.push_directions["down"] and entity.speed_y > 0:
                    self.speed_y = 1
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif self.push_directions["up"] and entity.speed_y < 0:
                    self.speed_y = -1
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x, self.rect.y))
##        pygame.draw.rect(layer, (255, 0, 0), self.rect)
##        pygame.draw.rect(layer, (0, 255, 0), (self.move_destination[0], self.move_destination[1], 10, 10))
