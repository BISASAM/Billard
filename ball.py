import sys, pygame
import numpy as np


class Ball():

    def __init__(self, screen, color, pos, radius):
        self.screen = screen
        self.color = color
        self.pos = np.array(pos)
        self.radius = radius
        self.v = np.zeros(2)
        self.r = np.zeros(2)
        self.collided = False

    def events(self):
        pass

    def update(self, elapsed_time):
        if np.linalg.norm(self.v) > 0.01:
            self.pos = self.pos + self.v * elapsed_time
            self.v *= 0.9985
        else:
            self.v = 0

    def draw(self):
        draw_pos = self.pos - np.array([self.radius/2, self.radius/2])
        pygame.draw.circle(self.screen, self.color, draw_pos.astype(int), self.radius)

    def move(self, velocity):
        self.v = np.asarray(velocity)
