import pygame, time, sys

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=64)
pygame.init()

screen = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

fps = 60

bpm = 103

key = False

color = (20, 70, 20)

beat_counter = 0

beats_pressed = 0

total_beats = 1

clap = pygame.mixer.Sound("Ste Ingham Synthwave Clap 01.wav")
kick = pygame.mixer.Sound("Ste Ingham Synthwave Kick 04.wav")
shaker = pygame.mixer.Sound("shaker-analog.wav")

shaker.set_volume(0.5)

drum_beat = [clap, None, shaker, None, kick, None, shaker, None]

BEAT_EVENT = pygame.USEREVENT + 1

active = False

while 1:

    # check events
    key = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                key = True
        if event.type == BEAT_EVENT:
            if beat_counter == 7:
                beat_counter = 0
                total_beats += 1
            else:
                beat_counter += 1
                
            if drum_beat[beat_counter] != None:
                drum_beat[beat_counter].play()

            if beat_counter == 0:
                color = (20, 70, 20)
            elif beat_counter == 4:
                color = (70, 20, 40)
        
    # check input is on beat
    if beat_counter in [0, 1, 7]:
        if key:
            beats_pressed += 1
            color = (200, 170, 90)
            if not(active):
                pygame.time.set_timer(BEAT_EVENT, int((60/bpm)*1000/4))
                active = True
        
    

    # render
    screen.fill(color)
    pygame.display.update()
    clock.tick(fps)
    
