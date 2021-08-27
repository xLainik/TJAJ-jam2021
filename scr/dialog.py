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

        self.skip = True
        self.skip_cooldown = 0

        self.black_rect = pygame.Rect((27 * self.game.SCALE, 210 * self.game.SCALE, 426 * self.game.SCALE, 48 * self.game.SCALE))

        self.name_speaker = "Null"
        self.name_color = (220, 70, 20)
        self.first_line = "First_line"
        self.second_line = "Second_line"

        self.name_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 12, self.name_speaker, self.name_color, True, self.black_rect.x + 40 * self.game.SCALE, self.black_rect.y + 14 * self.game.SCALE, True, self.game.SCALE)
        self.first_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.first_line, (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 10 * self.game.SCALE, False, self.game.SCALE)
        self.second_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.second_line, (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 28 * self.game.SCALE, False, self.game.SCALE)
        
    def update(self):
        if self.active:
            print("DIALOG START")
            while self.timer < self.max_timer:
                
                for key, line in self.dialog_queue.items():
                    if self.skip and self.timer > line[0] and self.timer <= line[0] + 40:
                        print("hola")
                        self.skip_cooldown += self.game.delta_time
                        if self.skip_cooldown >= 40:
                            self.skip_cooldown = 0
                            self.skip = False
                        self.current_line = line
                        self.next_line = self.dialog_queue[int(key) + 1]
                        self.name_txt.update(content = line[1], colour = line[2])
                        self.first_line_txt.update(content = line[3])
                        self.second_line_txt.update(content = line[4])
                if self.timer >= self.min_timer:
                    pygame.draw.rect(self.game.high_res_canvas, (20,20,20), self.black_rect)
                    if self.timer >= self.current_line[0] and self.timer < self.next_line[0]:
                        self.name_txt.update(self.game.high_res_canvas)
                        self.first_line_txt.update(self.game.high_res_canvas)
                        self.second_line_txt.update(self.game.high_res_canvas)
                        self.timer += self.game.delta_time
                        # insta skip dialog or speed it up
                        if self.game.actions[pygame.K_z] and self.skip_cooldown == 0:
                            self.timer = self.next_line[0] + 1
                            self.skip = True
                    if self.timer >= self.next_line[0]:
                        # skip to next dialog
                        if self.game.actions[pygame.K_z]:
                            self.timer = self.next_line[0]
                            self.skip = True
                        
                else:
                    self.game.high_res_canvas.fill((0,0,0))
                    pygame.draw.rect(self.game.high_res_canvas, (200,200,200), self.black_rect)

                
                self.game.render()
                
            self.__init__(self.game, self.dialog_queue, self.dialog_name)
            self.game.high_res_canvas.fill((0,0,0))
            print("DIALOG FINISH")

