import pygame, os, json

from scr.utility.resize_image import resize

from scr.sprites.text import Text

from scr.utility.easying import easeOutBack

class Dialog():
    def __init__(self, game, dialog_queue, dialog_name, level_number, images_json, must_action = True, bg = False) -> None:
        self.game = game

        self.dialog_name = dialog_name
        self.level_number = level_number
        self.images_json = images_json

        self.must_action = must_action
                        
        self.dialog_queue = dialog_queue
        # dict {[timer, talking name, talk name color, str(first line), str(second line)]} 

        self.active = False
        self.timer = 0

        self.bg = bg

        self.gameplay_screen = self.game.screen.copy()
        
        self.black_bg_img = pygame.Surface((game.SCREEN_WIDTH*game.SCALE, game.SCREEN_HEIGHT*game.SCALE))
        self.black_bg_img.set_alpha(50)

        self.max_timer = list(self.dialog_queue.values())[-1][0]

        with open(os.path.join("scr", "levels", "level_" + str(level_number), "level_" + str(level_number) + "_dialog_images", images_json), "r", encoding="utf-8") as dialog_img_json_file:

            json_file = json.load(dialog_img_json_file)

            # "key": [timer, screen_side, image.png to load] 
            self.img_sequence = []
            for key, sequence in json_file.items():
                if sequence[2] == "none":
                    self.img_sequence.append([sequence[0], sequence[1], pygame.image.load(os.path.join("scr", "assets", "images", "invisible.png")).convert()])
                else:
                    self.img_sequence.append([sequence[0], sequence[1], resize(pygame.image.load(os.path.join("scr", "assets", "images", "portraits", sequence[2])), self.game.SCALE, 4)])
                    
        for sequence in self.img_sequence:
            if sequence[1] == "right":
                self.current_img_right = sequence[2]
                break

        for sequence in self.img_sequence:
            if sequence[1] == "left":
                self.current_img_left = sequence[2]
                break

        self.skip_arrow_img = resize(pygame.image.load(os.path.join("scr", "assets", "images", "saltar.png")), self.game.SCALE, 4)
        self.espacio_txt = Text(self.game.high_res_canvas, os.path.join(self.game.font_directory,"hemi head bd it.ttf"), 12, "ESPACIO", (255,149,0), True, 380 * self.game.SCALE, 240 * self.game.SCALE, False, self.game.SCALE)
        
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
                self.game.screen.blit(pygame.transform.scale(self.game.game_canvas, (self.game.SCREEN_WIDTH * self.game.SCALE, self.game.SCREEN_HEIGHT * self.game.SCALE)), (0, 0))
                
                self.game.high_res_canvas.blit(self.current_img_left, (-58 * self.game.SCALE, 30 * self.game.SCALE))

                self.game.high_res_canvas.blit(self.current_img_right, (220 * self.game.SCALE, 30 * self.game.SCALE))
                
                if self.bg == False:
                    self.game.screen.blit(self.black_bg_img, (0, 0))
                pygame.draw.rect(self.game.high_res_canvas, (20,20,20), self.black_rect)
                pygame.draw.rect(self.game.high_res_canvas, (100, 100, 100), self.black_rect, width = (2 * self.game.SCALE))
                self.name_txt.update()
                self.first_line_txt.update()
                self.second_line_txt.update()

                # Skip button
                if self.timer >= self.current_line[0]:
                    pygame.draw.rect(self.game.high_res_canvas, (255,149,0), self.black_rect, width = (2 * self.game.SCALE))
                    self.game.high_res_canvas.blit(self.skip_arrow_img, (434 * self.game.SCALE, 240 * self.game.SCALE))
                    self.espacio_txt.update()

                self.game.screen.blit(self.game.high_res_canvas, (0,0))

                pygame.display.update()
                self.game.clock.tick(self.game.MAX_FPS)
                     

            self.__init__(self.game, self.dialog_queue, self.dialog_name, self.level_number, self.images_json, self.must_action, self.bg)
            self.game.high_res_canvas.fill((0,0,0))

