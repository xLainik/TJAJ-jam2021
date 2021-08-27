import pygame, os

from scr.utility.resize_image import resize

from scr.sprites.text import Text

from scr.utility.easying import easeOutBack

class Dialog():
    def __init__(self, game, dialog_queue, dialog_name) -> None:
        self.game = game

        self.dialog_name = dialog_name

                        
        self.dialog_queue = dialog_queue
        # dict {[timer, talking name, talk name color, str(first line), str(second line)]}

        self.active = False
        self.timer = 0
        self.min_timer = list(self.dialog_queue.values())[0][0]
        self.max_timer = list(self.dialog_queue.values())[-1][0]

        self.current_line = False
        self.next_line = False

        self.can_skip = False
        self.skip_cooldown = 0

##        print(self.dialog_queue)

        self.black_rect = pygame.Rect((27 * self.game.SCALE, 210 * self.game.SCALE, 426 * self.game.SCALE, 48 * self.game.SCALE))
        self.white_rect = pygame.Rect((400 * self.game.SCALE, 230 * self.game.SCALE, 20 * self.game.SCALE, 20 * self.game.SCALE))

        self.current_line = self.dialog_queue["0"]
        self.next_line = self.dialog_queue["1"]

        self.current_line_int = 0
        

        self.name_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 12, self.current_line[1], self.current_line[2], True, self.black_rect.x + 40 * self.game.SCALE, self.black_rect.y + 14 * self.game.SCALE, True, self.game.SCALE)
        self.first_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.current_line[3], (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 10 * self.game.SCALE, False, self.game.SCALE)
        self.second_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.current_line[4], (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 28 * self.game.SCALE, False, self.game.SCALE)

    def update(self):
        if self.game.actions[pygame.K_z] and self.active:
            print("DIALOG START")
            while self.timer < self.max_timer:
                print(self.timer)
                if self.timer < self.current_line[0]:
                    self.timer += self.game.delta_time
                elif self.can_skip and self.skip_cooldown == -1:
                    # skip to next dialog
                    if self.game.actions[pygame.K_z] and self.current_line_int + 2 < len(self.dialog_queue):
                        self.current_line_int += 1
                        self.can_skip = False
                        self.skip_cooldown = 0
                        for key, line in self.dialog_queue.items():
                            if self.timer < line[0]:
                                self.current_line = line
                                self.next_line = self.dialog_queue[str(int(key) + 1)]
                                self.name_txt.update(content = line[1], colour = line[2])
                                self.first_line_txt.update(content = line[3])
                                self.second_line_txt.update(content = line[4])
                                break
                if self.skip_cooldown >= 0:
                    self.skip_cooldown += self.game.delta_time
                    if self.skip_cooldown >= 20:
                        self.skip_cooldown = -1
                if self.timer >= 0:
                    pygame.draw.rect(self.game.high_res_canvas, (20,20,20), self.black_rect)
                    if self.timer < self.next_line[0]:
                        self.name_txt.update(self.game.high_res_canvas)
                        self.first_line_txt.update(self.game.high_res_canvas)
                        self.second_line_txt.update(self.game.high_res_canvas)
                    if not(self.can_skip) and self.skip_cooldown == -1:
                        pygame.draw.rect(self.game.high_res_canvas, (210,210,210), self.white_rect)
                        self.game.check_inputs()
                        # speed up dialog
##                        if self.game.actions[pygame.K_z]:
##                            pass
                        if self.timer > self.current_line[0]:
                            self.can_skip = True
                else:
                    self.game.high_res_canvas.fill((0,0,0))
                    pygame.draw.rect(self.game.high_res_canvas, (200,200,200), self.black_rect)
                    self.timer += self.game.delta_time

                
                self.game.render()
                
            self.__init__(self.game, self.dialog_queue, self.dialog_name)
            self.game.high_res_canvas.fill((0,0,0))
            print("DIALOG FINISH")

