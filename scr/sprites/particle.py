import pygame, math

class Particle():
    def __init__(self, tilemap, rect, animation: list, loop: bool, offset: tuple, particle_num: int, max_timer: int, interval: list, speed: float, gravity: bool):

        self.tilemap = tilemap
        self.rect = rect
        self.max_timer = max_timer

        self.gravity = gravity

        self.pick_up = False

        self.ani_timer = 0
        self.ani_frame = 0

        self.animation = [animation, loop, offset]  # [[animation], Loop boolean, (x,y render offset)]
        
        self.particles = []

        for i in range(1, particle_num + 1):
            if i == 1: angle = interval[0]
            else: angle = interval[0] + (interval[1] - interval[0])*(i-1)/(particle_num-1)
            sprite = pygame.sprite.Sprite()
            sprite.rect = self.rect
            sprite.rect.topleft = self.rect.topleft
            self.particles.append([sprite, rect.x, rect.y, speed*math.cos(angle), speed*-math.sin(angle)])

        self.timer = 0

    def update(self, tiles, rect, ass, first_update):
        if first_update:
            for particle in self.particles:
                particle[1] += particle[3] * self.tilemap.level.state.game.delta_time
                particle[2] += particle[4] * self.tilemap.level.state.game.delta_time

                if self.gravity:
                    # pseudo gravity
                    particle[4] += 0.05 * self.tilemap.level.state.game.delta_time

                particle[0].rect.x, particle[0].rect.y = int(particle[1]), int(particle[2])

            self.timer += self.tilemap.level.state.game.delta_time

    def draw(self, layer):
        for particle in self.particles:
            layer.blit(self.animation[0][self.ani_frame][0], (particle[0].rect.x-self.animation[2][0], particle[0].rect.y-self.animation[2][1]))
            #pygame.draw.rect(self.tilemap.level.state.game.game_canvas, (250,0,0), self.tilemap.level.camera.apply(particle[0]), width=2)

        if self.ani_timer < self.animation[0][self.ani_frame][1]:
            self.ani_timer += self.tilemap.level.state.game.delta_time
        else:
            self.ani_timer = 0
            self.ani_frame += 1
        if self.ani_frame >= len(self.animation[0]):
            self.ani_timer, self.ani_frame = 0, 0
