from scenebase import SceneBase
import pygame
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from tools import Tools, Color
from elements import Ball, Queue, Hole, Power


vel = 0.5

class GameScene(SceneBase):
    def __init__(self, screen, game_mode):
        SceneBase.__init__(self)
        self.screen = screen


        # create holes and balls
        self.hole_list = Tools.create_holes(self.screen)
        self.ball_list = Tools.create_balls(self.screen, game_mode)
        self.white_ball = [ball for ball in self.ball_list if ball.id == 0][0]
        self.collision_combination = Tools.jederMitJedem(self.ball_list)

        # create Queue
        self.queue = Queue(self.screen)

        # create Powerscale
        self.power = Power(max_power=5)

    def ProcessInput(self, events, pressed_keys, elapsed_time):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
    
        if not self.white_ball.is_moving:
            if pressed_keys[pygame.K_RIGHT]:
                self.queue.rotate(3, elapsed_time)
            if pressed_keys[pygame.K_LEFT]:
                self.queue.rotate(-3, elapsed_time)
            if pressed_keys[pygame.K_UP]:
                self.queue.rotate(-0.3, elapsed_time)
            if pressed_keys[pygame.K_DOWN]:
                self.queue.rotate(0.3, elapsed_time)
            if pressed_keys[pygame.K_SPACE]:
                self.power.load(0.01)
            for event in events:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    p = self.power.get()
                    self.white_ball.move(self.queue.get_r() * p)

    def Update(self, elapsed_time):

        for ball in self.ball_list:
            if not ball.holed:
                ball.update(elapsed_time)   # move ball
                Ball.ball_to_border_collision(*self.screen.get_size(), ball)  # border collisions
                for hole in self.hole_list:  # hole collisions
                    hole.collision(ball)

        for combi in self.collision_combination:
            Ball.ball_to_ball_collision(*combi)
        
        if self.white_ball.holed:  # if white_ball is holed, find a new place to place it
            new_pos = Tools.find_free_pos(self.ball_list)
            self.white_ball.pos = new_pos
            self.white_ball.holed = False
            self.white_ball.stop()

    def Render(self):
        Tools.draw_table(self.screen)
        for hole in self.hole_list:
            hole.draw()
        for ball in self.ball_list:
            ball.draw()

        if not self.white_ball.is_moving and not self.white_ball.holed:
            self.queue.draw(self.white_ball.pos)

        self.power.draw(self.screen, self.white_ball.pos)
