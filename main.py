import pygame as pyg
from time import time, sleep
import object

pyg.init()
monospace = pyg.font.SysFont("monospace", 15)

# Initial Width and Height
IWIDTH = 500
IHEIGHT = 500
WIDTH = IWIDTH
HEIGHT = IHEIGHT
FULLSCREEN = False
screen = pyg.display.set_mode((WIDTH, HEIGHT), pyg.DOUBLEBUF)

Player = object.Object(pyg.Rect(WIDTH/2, HEIGHT-50, 50, 50))
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
                Player.Velocity[1] += 7
            if event.key == pyg.K_RIGHT or event.key == pyg.K_LEFT:
                Player.Velocity[0] += 2 * (-1 if event.key == pyg.K_RIGHT else 1)
            if event.key == pyg.K_F11:
                FULLSCREEN = not FULLSCREEN
                pyg.display.quit()
                pyg.display.init()
                screen = pyg.display.set_mode((0 if FULLSCREEN else IWIDTH, 0 if FULLSCREEN else IHEIGHT), pyg.FULLSCREEN | pyg.DOUBLEBUF if FULLSCREEN else pyg.DOUBLEBUF)
                WIDTH = screen.get_width()
                HEIGHT = screen.get_height()
                del Player
                Player = object.Object(pyg.Rect(WIDTH/2, HEIGHT-50, 50, 50))
        if event.type == pyg.QUIT:
            running = False
    if Player.Rect.bottom < HEIGHT:
        # gravity should pull you down by a dynamic number every second
        # every (HEIGHT/54) px is a meter (i guess, i hate this part of code because it causes the square to have slow gravity above, which is realistic but in a 1920x1080 screen, it looks weird)
        # this was also why I put a ceiling, to stop it from flying up (seemingly) forever.
        Player.Velocity[1] -= 9.8*(P_Mass/((HEIGHT-Player.Rect.centery)/(HEIGHT/54)))*DT
        # pygame doesn't consider any number under 1 due to rounding
        # removed because we have a custom coordinate system that supports floating points.
        # if -0.75 < Player.Velocity[1] <= 0.75:
        #     Player.Velocity[1] = -Player.Velocity[1]
    # friction
    # if its grounded and there is vertical velocity and there is no horizontal velocity, apply friction
    if Player.Rect.bottom >= HEIGHT and (Player.Velocity[0] > 0 or Player.Velocity[0] < -0):
        Player.Velocity[0] *= 0.98
        if (Player.Velocity[0] < 1 and Player.Velocity[0] > -1):
            Player.Velocity[0] = 0
    # bouncing should apply if the ball is trying to crash into the floor/ceiling
    # while the side wall bouncing just sets the vertical velocity to the opposite, (xV*-1), this one is different as it should not be bouncing at the exact same speed as before.
    # Like in real life, if you threw something at the ground it would soon enough lose momentum and fall
    if Player.Rect.bottom > HEIGHT or Player.Rect.top < 0:
        if Player.Rect.bottom > HEIGHT:
            Player.Coordinates[1] = HEIGHT-50
        else:
            Player.Coordinates[1] = 0
#        Player.Velocity[0] = 0
        Player.Velocity[1] *= -1
        Player.Velocity[1] -= 2
    if Player.Rect.right > WIDTH or Player.Rect.left < 0:
        if Player.Rect.right > WIDTH:
            Player.Coordinates[0] = WIDTH-50
        else:
            Player.Coordinates[0] = 0
        Player.Velocity[0] *= -1
    if Player.Rect.bottom >= HEIGHT and (Player.Velocity[1] < 1 and Player.Velocity[1] > -1):
        Player.Coordinates[1] = HEIGHT-50
        Player.Velocity[1] = 0
    Player.Coordinates[0] += -Player.Velocity[0]
    Player.Coordinates[1] += -Player.Velocity[1]
    Player.Rect.x = Player.Coordinates[0]
    Player.Rect.y = Player.Coordinates[1]
    screen.fill((180, 180, 255))
    pyg.draw.rect(screen, Player.Color, Player.Rect, 0)
    label = monospace.render(f'{1/DT:.0f} FPS', True, (100, 100, 175))
    screen.blit(label, (0, 0))
    pyg.display.flip()
    DT = time()-_DT
pyg.quit()