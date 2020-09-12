from scenebase import SceneBase
import pygame
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from tools import Tools
from elements import Ball, Queue, Hole, Power


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
        self.hole_koord = [
            (b_thickness, b_thickness),
            (width // 2, b_thickness),
            (width - b_thickness, b_thickness),
            (b_thickness, height - b_thickness),
            (width // 2, height - b_thickness),
            (width - b_thickness, height - b_thickness)]

        # create holes and balls
        self.hole_list = Tools.create_holes(self.screen)
        self.ball_list = Tools.create_balls(self.screen, "8ball")
        self.white_ball = [ball for ball in self.ball_list if ball.id == 0][0]
        self.collision_combination = Tools.jederMitJedem(self.ball_list)

        # create Queue
        self.Q = Queue(self.screen)

        # powerscale
        self.power = Power(max_power=5)

    def ProcessInput(self, events, pressed_keys, elapsed_time):
        if not self.white_ball.is_moving:
            if pressed_keys[pygame.K_RIGHT]:
                self.Q.rotate(3, elapsed_time)
            if pressed_keys[pygame.K_LEFT]:
                self.Q.rotate(-3, elapsed_time)
            if pressed_keys[pygame.K_UP]:
                self.Q.rotate(-0.3, elapsed_time)
            if pressed_keys[pygame.K_DOWN]:
                self.Q.rotate(0.3, elapsed_time)
            if pressed_keys[pygame.K_SPACE]:
                self.power.load(0.01)
            for event in events:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    p = self.power.get()
                    self.white_ball.move(self.Q.get_r() * p)

    def Update(self, elapsed_time):

        for ball in self.ball_list:
            ball.update(elapsed_time)

        for combi in self.collision_combination:
            Ball.ball_to_ball_collision(*combi)

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

        self.power.draw(self.screen, self.white_ball.pos)

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

        width, height = self.screen.get_size()
        #arrow(self.screen, (40, 96))
        #arrow(self.screen, (width - 40, height - 96))
        #arrow(self.screen, (96, 40))
        #arrow(self.screen, (width - 96, height - 40))
        # arrow(self.screen, (1626, 798))


def arrow(screen, pos):
    arrow = [(0, 0), (20, 0), (20, 10)]
    arrow = [(point[0]+pos[0], point[1]+pos[1]) for point in arrow]
    pygame.draw.polygon(screen, red, arrow)


def ball_to_border_collision(width, height, b):

    if not b.holed:

        # collision with left and right border
        if 82 < b.pos[1] < height - 82:
            if b.pos[0] < 60 or b.pos[0] > width - 60:
                # reset position
                b.pos[0] = 60 if b.pos[0] < 60 else width - 60

                v_new = np.array([-b.v[0], b.v[1]])
                b.move(v_new)

        # collision with upper and lower border
        if 82 < b.pos[0] < width - 82:
            if b.pos[1] < 60 or b.pos[1] > height - 60:
                # reset position
                b.pos[1] = 60 if b.pos[1] < 60 else height - 60

                v_new = np.array([b.v[0], -b.v[1]])
                b.move(v_new)


def ball_to_hole_collision(b, hole_koord):
    if not b.holed:
        for koord in hole_koord:
            if np.linalg.norm(b.pos - np.array(koord)) < 30:
                b.holed = True
                break
