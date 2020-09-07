from scenebase import SceneBase
import pygame
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from tools import Tools
from elements import Ball, Queue, Hole


black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
brown = (102, 64, 0)
green = (0, 153, 0)

vel = 0.5


class GameScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen

        b_thickness = 40
        hole_radius = 40
        width, height = self.screen.get_size()
        self.hole_koord = [(b_thickness, b_thickness), (width//2, b_thickness), (width-b_thickness, b_thickness),
                           (b_thickness, height-b_thickness), (width//2, height-b_thickness), (width-b_thickness, height-b_thickness)]

        # create holes and balls
        self.hole_list = Tools.create_holes(self.screen)
        self.ball_list = Tools.create_balls(self.screen, "8ball")
        self.white_ball = [ball for ball in self.ball_list if ball.id == 0][0]
        self.collision_combination = Tools.jederMitJedem(self.ball_list)

        # create Queue
        self.Q = Queue(self.screen)

    def ProcessInput(self, events, pressed_keys):
        if not self.white_ball.is_moving:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.white_ball.move(self.Q.get_r()*vel)
            if pressed_keys[pygame.K_a]:
                    self.Q.rotate(clockwise=False)
            if pressed_keys[pygame.K_s]:
                    self.Q.rotate(clockwise=True)

    def Update(self, elapsed_time):

        for ball in self.ball_list:
            ball.update(elapsed_time)

        for combi in self.collision_combination:
            ball_to_ball_collision(*combi)

        for ball in self.ball_list:
            ball_to_border_collision(*self.screen.get_size(), ball)

        for ball in self.ball_list:
            for hole in self.hole_list:
                hole.collision(ball)

    def Render(self):
        self.screen.fill(green)
        Tools.draw_table(self.screen)
        for hole in self.hole_list:
            hole.draw()
        for ball in self.ball_list:
            ball.draw()

        if not self.white_ball.is_moving:
            self.Q.draw(self.white_ball.pos)
        

        arrow(self.screen, (26, 54))
        arrow(self.screen, (54, 26))
        arrow(self.screen, (54, 82))
        arrow(self.screen, (82, 54))

        arrow(self.screen, (1654, 54))
        arrow(self.screen, (1626, 26))
        arrow(self.screen, (1626, 82))
        arrow(self.screen, (1597, 54))

        arrow(self.screen,  (54, 854))
        arrow(self.screen, (26, 826))
        arrow(self.screen, (82, 826))
        arrow(self.screen, (54, 798))

        arrow(self.screen, (1626, 854))
        arrow(self.screen, (1654, 826))
        arrow(self.screen, (1597, 826))
        arrow(self.screen, (1626, 798))


def arrow(screen, pos):
    arrow = [(0, 0), (20, 0), (20, 10)]
    arrow = [(point[0]+pos[0], point[1]+pos[1]) for point in arrow]
    pygame.draw.polygon(screen, red, arrow)


def ball_to_border_collision(width, height, b):

    if not b.holed:
        rect1 = (40 < b.pos[0] < width - 40) and (117 <
                                                  b.pos[1] < height - 117)
        rect2 = (117 < b.pos[0] < width -
                 117) and (40 < b.pos[1] < height - 40)
        allowed_area = rect1 or rect2

        if allowed_area:
            # check x axis
            if b.pos[0] < 60 or b.pos[0] > width - 60:
                # reset position
                b.pos[0] = 60 if b.pos[0] < 60 else width - 60

                v_new = np.array([-b.v[0], b.v[1]])
                b.move(v_new)

            # check y axis
            if b.pos[1] < 60 or b.pos[1] > height - 60:
                # reset position
                b.pos[1] = 60 if b.pos[1] < 60 else height - 60

                v_new = np.array([b.v[0], -b.v[1]])
                b.move(v_new)


def ball_to_ball_collision(b1, b2):

    if not b1.holed and not b2.holed:
        if np.linalg.norm(b1.pos - b2.pos) < 40:

            normale = (b2.pos - b1.pos)/np.linalg.norm(b1.pos - b2.pos)
            tangente = np.array([normale[1], -normale[0]])

            while np.linalg.norm(b1.pos - b2.pos) < 40:  # reset ball position
                b1.pos = b1.pos - normale  # -= doesn't work in all cases here

            A = np.vstack((normale, tangente)).T

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
