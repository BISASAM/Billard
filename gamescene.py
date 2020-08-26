from scenebase import SceneBase
import pygame
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from tools import Tools
from elements import Ball, Queue


black = (0, 0, 0)
yellow = (255,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
brown = (102, 64, 0)
green = (0, 153, 0)

class GameScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen
        self.width, self.height = 1680, 880  # spielfeldgröße 1600, 800

        b_thickness = 40
        hole_radius = 40
        self.hole_koord = [(b_thickness, b_thickness), (self.width//2, b_thickness), (self.width-b_thickness, b_thickness), (b_thickness, self.height-b_thickness), (self.width//2, self.height-b_thickness), (self.width-b_thickness, self.height-b_thickness)]


        # create balls
        self.ball_list = Tools.create_balls(self.screen, "8ball")
        self.collision_combination = jederMitJedem(self.ball_list)
        self.white_ball = [ball for ball in self.ball_list if ball.id == 0][0]

    def ProcessInput(self, events, pressed_keys):
        vel = 1.5
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.white_ball.move([-vel, 0])
                if event.key == pygame.K_RIGHT:
                    self.white_ball.move([vel, 0])
                if event.key == pygame.K_UP:
                    self.white_ball.move([0, -vel])
                if event.key == pygame.K_DOWN:
                    self.white_ball.move([0, vel])
        
    def Update(self, elapsed_time):
        #q.update(self.white_ball.pos)
        #q.draw()

        for ball in self.ball_list:
            ball.update(elapsed_time)
            ball.draw()

        for combi in self.collision_combination:
            ball_to_ball_collision(*combi)
        
        for ball in self.ball_list:
            ball_to_border_collision(self.width, self.height, ball)
        
        for ball in self.ball_list:
            ball_to_hole_collision(ball, self.hole_koord)
    
    def Render(self, screen):
        screen.fill(green)
        Tools.draw_table(screen)
        for ball in self.ball_list:
            ball.draw()

    
def jederMitJedem(liste):
    result = []
    start = 0
    for entry in liste:
        start += 1
        for i in range(start, len(liste)):
            result.append((entry, liste[i]))
    return result


def ball_to_border_collision(width, height, b):
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


def ball_to_hole_collision(b, hole_koord):
    if not b.holed:
        for koord in hole_koord:
            if np.linalg.norm(b.pos - np.array(koord)) < 30:
                b.holed = True
                break