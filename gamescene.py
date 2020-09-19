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
            if not ball.holed:
                ball.update(elapsed_time)
                Ball.ball_to_border_collision(*self.screen.get_size(), ball)
                for hole in self.hole_list:
                    hole.collision(ball)

        for combi in self.collision_combination:
            Ball.ball_to_ball_collision(*combi)

    def Render(self):
        self.screen.fill(green)
        Tools.draw_table(self.screen)
        for hole in self.hole_list:
            hole.draw()
        for ball in self.ball_list:
            ball.draw()

        if not self.white_ball.is_moving and not self.white_ball.holed:
            self.Q.draw(self.white_ball.pos)

        self.power.draw(self.screen, self.white_ball.pos)

def arrow(screen, pos):
    arrow = [(0, 0), (20, 0), (20, 10)]
    arrow = [(point[0]+pos[0], point[1]+pos[1]) for point in arrow]
    pygame.draw.polygon(screen, red, arrow)
