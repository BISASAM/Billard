import sys, pygame
import numpy as np
import math


class Ball:

    def __init__(self, screen, color, pos, radius):
        self.screen = screen
        self.color = color
        self.pos = np.array(pos)
        self.radius = radius
        self.v = np.zeros(2)
        self.r = np.zeros(2)
        self.holed = False

    def events(self):
        pass

    def update(self, elapsed_time):
        if np.linalg.norm(self.v) > 0.01:
            self.pos = self.pos + self.v * elapsed_time
            self.pos = np.mod(self.pos, [self.screen.get_width(), self.screen.get_height()]) 
            # self.v = self.v - self.v / np.linalg.norm(self.v) * 0.0003 * elapsed_time  # linear decreasing of v
            self.v *= math.pow(0.9985, elapsed_time)  # exponential decreasing of v
        else:
            self.v = np.zeros(2)

    def draw(self):
        if not self.holed:
            pygame.draw.circle(self.screen, self.color, self.pos.astype(int), self.radius)

    def move(self, velocity):
        self.v = np.array(velocity)


class Hole:

    def __init__(self, screen, pos, radius):
        self.screen = screen
        self.color = color
        self.pos = np.array(pos)
        self.radius = radius
        self.v = np.zeros(2)
        self.r = np.zeros(2)
        self.holed = False

    def events(self):
        pass

    def update(self, elapsed_time):
        if np.linalg.norm(self.v) > 0.01:
            self.pos = self.pos + self.v * elapsed_time
            self.pos = np.mod(self.pos, [self.screen.get_width(), self.screen.get_height()]) 
            # self.v = self.v - self.v / np.linalg.norm(self.v) * 0.0003 * elapsed_time  # linear decreasing of v
            self.v *= math.pow(0.9985, elapsed_time)  # exponential decreasing of v
        else:
            self.v = np.zeros(2)

    def draw(self):
        if not self.holed:
            pygame.draw.circle(self.screen, self.color, self.pos.astype(int), self.radius)

    def move(self, velocity):
        self.v = np.array(velocity)


class Queue:

    white = (255,255,255)

    def __init__(self, screen, pos):
         self.screen = screen
         self.start_pos = np.array([pos[0]-30, pos[1]]) 
         self.end_pos = np.array([self.start_pos[0]-150, self.start_pos[1]])

    def update(self, pos):
        self.start_pos =np.array([pos[0]-30, pos[1]]) 
        self.end_pos = np.array([self.start_pos[0]-150, self.start_pos[1]])

    def draw(self):
        global white
        pygame.draw.line(self.screen, (255,255,255), self.start_pos.astype(int), self.end_pos.astype(int), 5)

    def rotate(self, delta):
        self.v = np.array(velocity)