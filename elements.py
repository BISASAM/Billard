import sys
import pygame
import numpy as np
import math


black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
brown = (102, 64, 0)
green = (0, 153, 0)


class Ball:

    radius = 20  # class variable

    def __init__(self, id, screen, pos, txt):
        self.id = id
        self.screen = screen
        self.pos = np.array(pos)
        self.v = np.zeros(2)
        self.r = np.zeros(2)
        self.holed = False
        self.image = pygame.transform.scale(pygame.image.load(txt), (40, 40))
        self.is_moving = False

    def __str__(self):
        return f"(Ball {self.id} @ {self.pos})"

    def __repr__(self):
        return f"(Ball {self.id} @ {self.pos})"

    def events(self):
        pass

    def update(self, elapsed_time):
        if np.linalg.norm(self.v) > 0.01:
            # update for every millisecond to ensure same ball speed on different client performance
            for ms in range(0, elapsed_time):
                self.pos = self.pos + self.v
                self.v *= 0.9985
                self.pos = np.mod(
                    self.pos, [self.screen.get_width(), self.screen.get_height()])
        else:
            self.v = np.zeros(2)
            self.is_moving = False

    def draw(self):
        if not self.holed:
            # origin_shift to center of ball
            new_pos = np.array(
                [self.pos[0]-Ball.radius, self.pos[1]-Ball.radius]).astype(int)
            self.screen.blit(self.image, new_pos)

    def move(self, velocity):
        self.is_moving = True
        self.v = np.array(velocity)

    # getter to easily adress x and y koordinate
    def get_x(self):
        print("Getting x")
        return self.pos[0]

    def get_y(self):
        print("Getting y")
        return self.pos[1]
    
    x = property(get_x)
    y = property(get_y)

    @staticmethod
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


class Hole:

    def __init__(self, screen, pos, radius, typ):
        """Summary or Description of the Function

            Parameters:
            type (string): ul for upper left hole
                           um for upper mid hole
                           ur for upper right hole
                           ll for lower left hole
                           lm for lower mid hole
                           lr for lower right hole
        """

        self.screen = screen
        self.pos = np.array(pos)
        self.radius = radius
        self.typ = typ

        # props for ball to hole collisions, AC -> lower line, BD -> upper line
        A, B, C, D = (0, 0), (0, 0), (1, 0), (1, 0)
        if typ == "ul":
            A = (26, 54)
            B = (54, 26)
            C = (54, 82)
            D = (82, 54)

        elif typ == "ur":
            A = (1654, 54)
            B = (1626, 26)
            C = (1626, 82)
            D = (1597, 54)

        elif typ == "ll":
            A = (54, 854)
            B = (26, 826)
            C = (82, 826)
            D = (54, 798)

        elif typ == "lr":
            A = (1626, 854)
            B = (1654, 826)
            C = (1597, 826)
            D = (1626, 798)

        # lines defining hole entry
        self.lower_line = Line(A, C)
        self.upper_line = Line(B, D)

    def collision(self, ball):

        if self.typ not in ["um", "lm"] and not ball.holed:
            if self.lower_line.is_below_line(ball.pos) or self.upper_line.is_above_line(ball.pos):
                # reset position
                while self.lower_line.is_below_line(ball.pos) or self.upper_line.is_above_line(ball.pos):
                    ball.pos = ball.pos - ball.v

                v_new = np.array([ball.v[1], ball.v[0]])
                ball.move(v_new)

    def draw(self):
        pygame.draw.circle(self.screen, black, self.pos, self.radius)

        if self.typ == "ul":  # upper left
            pygame.draw.polygon(self.screen, black, [(12, 68), (40, 40), (68, 12), (96, 40), (40, 96)])
        elif self.typ == "ur":  # upper right
            ur = [(12, 12), (40, 40), (68, 68), (40, 96), (-16, 40)]
            ur = [(point[0] + 1600, point[1]) for point in ur]
            pygame.draw.polygon(self.screen, black, ur)
        elif self.typ == "ll":  # lower left
            ll = [(12, 12), (40, 40), (68, 68), (96, 40), (40, -16)]
            ll = [(point[0], point[1] + 800) for point in ll]
            pygame.draw.polygon(self.screen, black, ll)
        elif self.typ == "lr":  # lower right
            lr = [(12, 68), (40, 40), (68, 12), (40, -16), (-16, 40)]
            lr = [(point[0] + 1600, point[1] + 800) for point in lr]
            pygame.draw.polygon(self.screen, black, lr)


class Line:
    """Helper class to do collisions with diagonal lines of corner holes"""

    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
        self.f_x = Line.compute_line(P, Q)

    def compute_line(P, Q):
        a = np.array([[P[0], 1], [Q[0], 1]])
        b = np.array([P[1], Q[1]])
        slope, c = np.linalg.solve(a, b)
        def f(x): return slope*x + c
        return f

    def is_above_line(self, point):
        in_x_area = min(self.P[0], self.Q[0]) < point[0] < max(
            self.P[0], self.Q[0])
        in_y_area = min(self.P[1], self.Q[1]) < point[1] < max(
            self.P[1], self.Q[1])
        if in_x_area and in_y_area:
            return point[1] > self.f_x(point[0])
        else:
            return False

    def is_below_line(self, point):
        in_x_area = min(self.P[0], self.Q[0]) < point[0] < max(
            self.P[0], self.Q[0])
        in_y_area = min(self.P[1], self.Q[1]) < point[1] < max(
            self.P[1], self.Q[1])
        if in_x_area and in_y_area:
            return point[1] < self.f_x(point[0])
        else:
            return False


class Queue:

    white = (255, 255, 255)

    def __init__(self, screen):
        self.screen = screen

        #self.edges = [np.array((20, 30)), np.array((20, 40)), np.array((400, 38)), np.array((400, 32))]
        self.edges = [np.array((30, 32)), np.array((30, 38)), np.array((150, 38)), np.array((150, 32))]
        self.pivot = np.array([0, 35])

        # Rotation matrix, initial values
        self.theda = 15
        scale = self.theda / 1000
        self.rot = np.array(((np.cos(scale), -np.sin(scale)), (np.sin(scale), np.cos(scale))))

    def update(self, pos):
        pass

    def draw(self, ball_pos):
        translation = self.edges + ball_pos - self.pivot
        pygame.draw.polygon(self.screen, white, translation)

    def rotate(self, rot_speed, elapsed_time):
        if rot_speed != self.theda:
            self.update_rot_mat(rot_speed)

        for ms in range(0, elapsed_time):  # for equal speed on diff. machines
            self.edges = self.edges - self.pivot
            new_edges = []
            for point in self.edges:
                new_edges.append(np.dot(self.rot, point))
            self.edges = new_edges + self.pivot

    def get_r(self):
        r = self.edges[2] - self.edges[0]
        return r / np.linalg.norm(r)
    
    def update_rot_mat(self, rot_speed):
        self.theda = rot_speed
        scale = self.theda / 1000
        self.rot = np.array(((np.cos(scale), -np.sin(scale)), (np.sin(scale), np.cos(scale))))


class Power:

    def __init__(self, max_power):
        self.power = 0
        self.max_power = max_power
        self.active = False

    def load(self, amount):
        if not self.active: 
            self.active = True
        self.power += amount
        self.power = min(self.power, self.max_power)

    def get(self):
        power = self.power
        self.reset()
        return power

    def reset(self):
        self.active = False
        self.power = 0

    def draw(self, screen, ball_pos):
        if self.active:
            color = (self.power/self.max_power * 255, 0, (1-self.power/self.max_power) * 255)
            pos = np.array([10, -40]) + ball_pos
            width = (self.power * 30, 10)
            pygame.draw.rect(screen, black, [*pos, self.max_power*30, 10], 2)
            pygame.draw.rect(screen, color, [*pos, *width])
