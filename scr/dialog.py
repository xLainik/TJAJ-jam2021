import pygame, os

from scr.utility.resize_image import resize

from scr.sprites.text import Text

from scr.utility.easying import easeOutBack

class Dialog():
    def __init__(self, game, dialog_queue, dialog_name, must_action = True) -> None:
        self.game = game

        self.dialog_name = dialog_name

        self.must_action = must_action
                        
        self.dialog_queue = dialog_queue
        # dict {[timer, talking name, talk name color, str(first line), str(second line)]}

        self.active = False
        self.timer = 0

        self.max_timer = list(self.dialog_queue.values())[-1][0]

        self.current_line = False
        self.next_line = False

        self.black_rect = pygame.Rect((27 * self.game.SCALE, 210 * self.game.SCALE, 426 * self.game.SCALE, 48 * self.game.SCALE))
        self.white_rect = pygame.Rect((400 * self.game.SCALE, 230 * self.game.SCALE, 20 * self.game.SCALE, 20 * self.game.SCALE))

        self.current_line = self.dialog_queue["0"]
        self.next_line = self.dialog_queue["1"]

        self.current_line_int = 1

        self.name_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 12, self.current_line[1], self.current_line[2], True, self.black_rect.x + 40 * self.game.SCALE, self.black_rect.y + 14 * self.game.SCALE, True, self.game.SCALE)
        self.first_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.current_line[3], (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 10 * self.game.SCALE, False, self.game.SCALE)
        self.second_line_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"Monitorica-Bd.ttf"), 12, self.current_line[4], (200,200,200), True, self.black_rect.x + 80 * self.game.SCALE, self.black_rect.y + 28 * self.game.SCALE, False, self.game.SCALE)

    def update(self):
        if (self.must_action and self.game.actions["space"]) or (self.must_action == False):
            while self.timer < self.max_timer:
                if self.timer < self.current_line[0]:
                    self.timer += self.game.delta_time
                else:
                    self.game.check_inputs()
                    if bool(self.game.actions["space"]):
                        if not(self.next_line[1] == " "):
                            self.current_line = self.next_line
                            self.next_line = self.dialog_queue[str(self.current_line_int + 1)]
                            self.name_txt.update(content = self.current_line[1], colour = self.current_line[2])
                            self.first_line_txt.update(content = self.current_line[3])
                            self.second_line_txt.update(content = self.current_line[4])
                            self.current_line_int += 1
                        else:
                            self.timer = self.max_timer
                    
                # mostrar dialogo actual
                pygame.draw.rect(self.game.high_res_canvas, (20,20,20), self.black_rect)
                self.name_txt.update()
                self.first_line_txt.update()
                self.second_line_txt.update()

                if self.timer >= self.current_line[0]:
                    pygame.draw.rect(self.game.high_res_canvas, (210,210,210), self.white_rect)
                     
                self.game.render()
                
            self.__init__(self.game, self.dialog_queue, self.dialog_name, self.must_action)
            self.game.high_res_canvas.fill((0,0,0))

