import sys
import pygame
import numpy as np
from elements import Ball, Queue


black = (0, 0, 0)
yellow = (255,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
brown = (102, 64, 0)
green = (0, 153, 0)

size = width, height = 1680, 880  # spielfeldgröße 1600, 800

b_thickness = 40
hole_radius = 40
hole_koord = [(b_thickness, b_thickness), (width//2, b_thickness), (width-b_thickness, b_thickness), (b_thickness, height-b_thickness), (width//2, height-b_thickness), (width-b_thickness, height-b_thickness)]

def start():
    pygame.init()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # create balls
    w_ball = Ball(screen, white, [200, 400], 20)
    y_ball = Ball(screen, yellow, [600, 400], 20)
    r_ball = Ball(screen, red, [640, 422], 20)
    b_ball = Ball(screen, blue, [640, 378], 20)
    b1_ball = Ball(screen, blue, [680, 400], 20)
    b2_ball = Ball(screen, blue, [680, 442], 20)
    b3_ball = Ball(screen, blue, [680, 358], 20)

    ball_list = [w_ball, y_ball, r_ball, b_ball, b1_ball, b2_ball, b3_ball]
    collision_combination = jederMitJedem(ball_list)

    #y_ball.move([-1., 0])

    q = Queue(screen, w_ball.pos)
    
    while True:
        #print('frame begins')
        screen.fill(green)
        draw_border(screen)

        # events
        vel = .5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    w_ball.move([-vel, 0])
                if event.key == pygame.K_RIGHT:
                    w_ball.move([vel, 0])
                if event.key == pygame.K_UP:
                    w_ball.move([0, -vel])
                if event.key == pygame.K_DOWN:
                    w_ball.move([0, vel])

        

        # updates
        elapsed_time = clock.tick()

        q.update(w_ball.pos)
        q.draw()

        for ball in ball_list:
            ball.update(elapsed_time)
            ball.draw()

        for combi in collision_combination:
            ball_to_ball_collision(*combi)
        
        for ball in ball_list:
            ball_to_border_collision(ball)
        
        for ball in ball_list:
            ball_to_hole_collision(ball)

        pygame.display.flip()
        #print('frame ends')


def draw_border(screen):
    global b_thickness
    global hole_radius
    #borders
    pygame.draw.rect(screen, brown, (0, 0, width, b_thickness))
    pygame.draw.rect(screen, brown, (0, height-b_thickness,width, b_thickness))
    pygame.draw.rect(screen, brown, (0, 0, b_thickness, height))
    pygame.draw.rect(screen, brown, (width-b_thickness, 0, b_thickness, height))

    # holes
    pygame.draw.circle(screen, black, (b_thickness, b_thickness), hole_radius)
    pygame.draw.circle(screen, black, (width//2, b_thickness), hole_radius)
    pygame.draw.circle(screen, black, (width-b_thickness, b_thickness), hole_radius)
    pygame.draw.circle(screen, black, (b_thickness, height-b_thickness), hole_radius)
    pygame.draw.circle(screen, black, (width//2, height-b_thickness), hole_radius)
    pygame.draw.circle(screen, black, (width-b_thickness, height-b_thickness), hole_radius)


def jederMitJedem(liste):
    result = []
    start = 0
    for entry in liste:
        start += 1
        for i in range(start, len(liste)):
            result.append((entry, liste[i]))
    return result


def ball_to_border_collision(b):
    if not b.holed:
        if b.pos[0] < 60 or b.pos[0] > width - 60:
            # reset position
            b.pos[0] = 60 if b.pos[0] < 60 else width - 60

            v_new = np.array([-b.v[0], b.v[1]])
            b.move(v_new)

        elif b.pos[1] < 60 or b.pos[1] > height - 60:
            # reset position
            b.pos[1] = 60 if b.pos[1] < 60 else height - 60

            v_new = np.array([b.v[0], -b.v[1]])
            b.move(v_new)


def ball_to_ball_collision(b1, b2):

    if not b1.holed and not b2.holed:
        if np.linalg.norm(b1.pos - b2.pos) < 40:

            normale = (b2.pos - b1.pos)/np.linalg.norm(b1.pos - b2.pos)
            tangente = np.array([normale[1], -normale[0]])

            while np.linalg.norm(b1.pos - b2.pos) < 40:
                b1.pos = b1.pos - normale  # -= doesn't work in all cases here

            A = np.vstack((normale,tangente)).T

            # split v1 into v1_n & v1_t 
            parameter = np.linalg.solve(A, b1.v)
            v1_n = normale * parameter[0]
            v1_t = tangente * parameter[1]

            # split v2 into v2_n & v2_t 
            parameter = np.linalg.solve(A, b2.v)
            v2_n = normale * parameter[0]
            v2_t = tangente * parameter[1]

            v1_new = v2_n + v1_t
            v2_new = v1_n + v2_t

            b1.move(v1_new)
            b2.move(v2_new)


def ball_to_hole_collision(b):
    if not b.holed:
        for koord in hole_koord:
            if np.linalg.norm(b.pos - np.array(koord)) < 30:
                b.holed = True
                break





if __name__ == "__main__":
    start()
    

