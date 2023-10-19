import pygame as pyg
from time import time, sleep

pyg.init()
monospace = pyg.font.SysFont("monospace", 15)

# Initial Width and Height
IWIDTH = 500
IHEIGHT = 500
WIDTH = IWIDTH
HEIGHT = IHEIGHT
FULLSCREEN = False
screen = pyg.display.set_mode((WIDTH, HEIGHT), pyg.DOUBLEBUF)

Player = pyg.Rect(WIDTH/2, HEIGHT-50, 50, 50)

P_Color = (255, 255, 255)
P_Velocity = [0, 0]
P_Coordinates = [WIDTH/2, HEIGHT-50]
# Kilograms
P_Mass = 20
running = True
DT = 1

while running:
    # NEVER use this.
    _DT = time()
    for event in pyg.event.get():
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                running = False
            if event.key == pyg.K_SPACE:
                P_Velocity[1] += 7
            if event.key == pyg.K_RIGHT or event.key == pyg.K_LEFT:
                P_Velocity[0] += 2 * (-1 if event.key == pyg.K_RIGHT else 1)
            if event.key == pyg.K_F11:
                FULLSCREEN = not FULLSCREEN
                pyg.display.quit()
                pyg.display.init()
                screen = pyg.display.set_mode((0 if FULLSCREEN else IWIDTH, 0 if FULLSCREEN else IHEIGHT), pyg.FULLSCREEN | pyg.DOUBLEBUF if FULLSCREEN else pyg.DOUBLEBUF)
                WIDTH = screen.get_width()
                HEIGHT = screen.get_height()
                del Player
                Player = pyg.Rect(WIDTH/2, HEIGHT-50, 50, 50)
                P_Coordinates = [WIDTH/2, HEIGHT-50]
        if event.type == pyg.QUIT:
            running = False
    if Player.bottom < HEIGHT:
        # gravity should pull you down by a dynamic number every second
        # every (HEIGHT/54) px is a meter (i guess, i hate this part of code because it causes the square to have slow gravity above, which is realistic but in a 1920x1080 screen, it looks weird)
        # this was also why I put a ceiling, to stop it from flying up (seemingly) forever.
        P_Velocity[1] -= (4.9 if 1 <= P_Velocity[0] or -1 >= P_Velocity[0] else 9.8)*(P_Mass/((HEIGHT-Player.centery)/(HEIGHT/54)))*DT
        # pygame doesn't consider any number under 1 due to rounding
        if -0.75 < P_Velocity[1] <= 0.75:
            P_Velocity[1] = -P_Velocity[1]
    # friction
    # if its grounded and there is vertical velocity and there is no horizontal velocity, apply friction
    if P_Coordinates[1] >= HEIGHT-50 and (P_Velocity[0] > 0 or P_Velocity[0] < -0) and not (P_Velocity[1] > 0 or P_Velocity[1] < -0):
        P_Velocity[0] *= 0.98
        if (P_Velocity[0] < 0.1 and P_Velocity[0] > -0.1):
            P_Velocity[0] = 0
    # bouncing should apply if the ball is trying to crash into the floor/ceiling
    # while the side wall bouncing just sets the vertical velocity to the opposite, (xV*-1), this one is different as it should not be bouncing at the exact same speed as before.
    # Like in real life, if you threw something at the ground it would soon enough lose momentum and fall
    elif Player.bottom > HEIGHT or Player.top < 0:
        if Player.bottom > HEIGHT:
            P_Coordinates[1] = HEIGHT-50
        else:
            P_Coordinates[1] = 0
#        P_Velocity[0] = 0
        P_Velocity[1] *= -.9
    if Player.right > WIDTH or Player.left < 0:
        if Player.right > WIDTH:
            P_Coordinates[0] = WIDTH-50
        else:
            P_Coordinates[0] = 0
        P_Velocity[0] *= -1
    if P_Coordinates[1] > HEIGHT-50.5 and (P_Velocity[1] < 1 and P_Velocity[1] > -1):
        P_Coordinates[1] = HEIGHT-50
        P_Velocity[1] = 0
    P_Coordinates[0] += -P_Velocity[0]
    P_Coordinates[1] += -P_Velocity[1]
    Player.x = P_Coordinates[0]
    Player.y = P_Coordinates[1]
    screen.fill((180, 180, 255))
    pyg.draw.rect(screen, P_Color, Player, 0)
    label = monospace.render(f'{1/DT:.0f} FPS', True, (100, 100, 175))
    screen.blit(label, (0, 0))
    pyg.display.flip()
    DT = time()-_DT
pyg.quit()