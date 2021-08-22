import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, entity_name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(x + 5, y + 5, 10, 10)
        self.x, self.y = self.rect.x, self.rect.y

        self.collided, self.moving = False, False

        self.entity_name = entity_name

    def update(self, entities, player_turn, delta_time):
        pass
    
    def draw(self, layer):
        layer.blit(self.image, (self.rect.x - 5, self.rect.y - 5))

class Barrier(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

    def update(self, entities, player_turn, delta_time):
        pass

class Table(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

    def update(self, entities, player_turn, delta_time):
        pass

class Box(Obstacle):
    def __init__(self, image, x, y, entity_name):
        super().__init__(image, x, y, entity_name)

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

        self.move_destination = -10, -10

    def update(self, entities, player_turn, delta_time):

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

        # Collision direction from the box reference point
        self.collision_directions = {"left": False, "right": False, "bottom": False, "top": False}

        self.rect.x = int(self.x)

        hit_list = pygame.sprite.spritecollide(self, entities, False)

        for entity in hit_list:
            if entity.entity_name == "barrera":
                if self.speed_x > 0:
                    self.rect.right = entity.rect.left
                    self.collision_directions["right"] = True
                elif self.speed_x < 0:
                    self.rect.left = entity.rect.right
                    self.collision_directions["left"] = True
                self.x = self.rect.x
            # The player pushed the box
            if entity.entity_name == "player" and not(self.moving):
                if entity.speed_x > 0:
                    self.speed_x = 1
                    self.moving = True
                    self.move_destination = self.rect.x + 20, self.rect.y
                elif entity.speed_x < 0:
                    self.speed_x = -1
                    self.moving = True
                    self.move_destination = self.rect.x - 20, self.rect.y
                elif entity.speed_y > 0:
                    self.speed_y = 1
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y + 20
                elif entity.speed_y < 0:
                    self.speed_y = -1
                    self.moving = True
                    self.move_destination = self.rect.x, self.rect.y - 20

        self.rect.y = int(self.y)
            
        hit_list = pygame.sprite.spritecollide(self, entities, False)
        
        for entity in hit_list:
            if entity.entity_name == "barrera":
                if self.speed_y > 0:
                    self.rect.bottom = entity.rect.top
                    self.collision_directions["bottom"] = True
                elif self.speed_y < 0:
                    self.rect.top = entity.rect.bottom
                    self.collision_directions["top"] = True
                self.y = self.rect.y
    
    def draw(self, layer):
        super().draw(layer)
        pygame.draw.rect(layer, (255, 0, 0), self.rect)
        pygame.draw.rect(layer, (0, 255, 0), (self.move_destination[0], self.move_destination[1], 10, 10))
