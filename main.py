import sys
import pygame
import numpy as np
from ball import Ball


pygame.init()

size = width, height = 800, 400
black = (0, 0, 0)
yellow = (255,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# create balls
w_ball = Ball(screen, white, [200, 200], 20)
y_ball = Ball(screen, yellow, [600, 180], 20)
r_ball = Ball(screen, red, [600, 230], 20)
#b_ball = Ball(screen, blue, [640, 220], 20)


def collision(b1, b2):
    if np.linalg.norm(b1.v) > 0:
        collided = b1.collided #or b2.collided
        if np.linalg.norm(b1.pos - b2.pos) < 39 and not collided:
            b1.collided = True
            #b2.collided = True
            v = np.linalg.norm(b1.v)
            normale = (b2.pos - b1.pos)/np.linalg.norm(b1.pos - b2.pos)
            tangente = np.array([normale[1], -normale[0]])
            alpha = np.arccos(np.dot(b1.v, tangente)/(np.linalg.norm(b1.v) * np.linalg.norm(tangente)))
            v_n = v * np.sin(alpha)
            v_t = v * np.cos(alpha)

            print('hit')
            b1.move(v_t * tangente)
            b2.move(v_n * normale)

        if np.linalg.norm(b1.pos - b2.pos) > 39 and collided:
            b1.collided = False
            #b2.collided = False


while True:

    screen.fill(black)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                w_ball.move([0.9, 0])



    # updates
    elapsed_time = clock.tick()

    w_ball.update(elapsed_time)
    y_ball.update(elapsed_time)
    r_ball.update(elapsed_time)
    #b_ball.update(elapsed_time)

    collision(w_ball, y_ball)
    #collision(w_ball, r_ball)
    #collision(y_ball, w_ball)
    #collision(y_ball, r_ball)
    #collision(r_ball, w_ball)
    #collision(r_ball, y_ball)



    # draws
    w_ball.draw()
    y_ball.draw()
    r_ball.draw()
    #b_ball.draw()

    pygame.display.flip()
