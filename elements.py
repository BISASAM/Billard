import sys
import pygame
import numpy as np
import math


# cant import tools.Color because of circular dependecies
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
brown = (102, 64, 0)
green = (0, 153, 0)
grey = (100, 100, 100)


class Ball:

    radius = 20  # class variable

    def __init__(self, id, screen, pos, image_pth):
        self.id = id
        self.screen = screen
        self._pos = np.array(pos)  # needs to be float, dont convert to int!
        self.v = np.zeros(2)
        self.r = np.zeros(2)
        self.holed = False
        self.image = pygame.transform.scale(pygame.image.load(image_pth), (40, 40))
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
                self.pos = np.mod(self.pos, [self.screen.get_width(), self.screen.get_height()])
        else:
            self.v = np.zeros(2)
            self.is_moving = False

    def draw(self):
        if not self.holed:
            # pos shift to upper left corner to draw ball_image
            new_pos = np.array(
                [self.pos[0]-Ball.radius, self.pos[1]-Ball.radius]).astype(int)
            self.screen.blit(self.image, new_pos)

    def move(self, velocity):
        self.is_moving = True
        self.v = np.array(velocity)
    
    def stop(self):
        self.v = np.zeros(2) 

    # getter, setter to easily adress x and y koordinate
    def get_x(self):
        return self.pos[0]
    
    def set_x(self, value):
        self.pos[0] = value % self.screen.get_width()

    def get_y(self):
        return self.pos[1]
    
    def set_y(self, value):
        self.pos[1] = value % self.screen.get_height()

    def get_pos(self):
        return self._pos
    
    def set_pos(self, koord):
        self._pos = np.array(koord)
    
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    pos = property(get_pos, set_pos)

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

    @staticmethod
    def ball_to_border_collision(width, height, b):
        if not b.holed:

            # collision with left and right border
            if 88 < b.y < height - 88:
                if b.x < 60 or b.x > width - 60:
                    # reset position
                    b.x = 60 if b.x < 60 else width - 60

                    v_new = np.array([-b.v[0], b.v[1]])
                    b.move(v_new)

            # collision with upper and lower border (leave out middle holes)
            if 88 < b.x <= 820 or 860 <= b.x < width - 88:
                if b.y < 60 or b.y > height - 60:
                    # reset position
                    b.y = 60 if b.y < 60 else height - 60

                    v_new = np.array([b.v[0], -b.v[1]])
                    b.move(v_new)


class Hole:

    def __init__(self, screen, pos, typ):
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
        self.radius = 40  # fix
        self.typ = typ

        # props for ball to hole collisions, AB -> upper line, CD -> lower line
        A, B, C, D = (0, 0), (1, 0), (0, 0), (1, 0)
        if typ == "ul":
            A = (54, 26)
            B = (88, 60)
            C = (26, 54)
            D = (60, 88)
            self.polygon = [(12, 68), (40, 40), (68, 12), (96, 40), (40, 96)]
            self.goal_line = Line(A,C)


        elif typ == "ur":
            A = (1591, 60)
            B = (1626, 26)
            C = (1620, 88)
            D = (1654, 54)
            self.polygon = [(12, 12), (40, 40), (68, 68), (40, 96), (-16, 40)]
            self.polygon = [(point[0] + 1600, point[1]) for point in self.polygon] 
            self.goal_line = Line(B,D)

        elif typ == "ll":
            A = (25, 826)
            B = (60, 791)
            C = (54, 854)
            D = (88, 820)
            self.polygon = [(12, 12), (40, 40), (68, 68), (96, 40), (40, -16)]
            self.polygon = [(point[0], point[1] + 800) for point in self.polygon] 
            self.goal_line = Line(A,C)

        elif typ == "lr":
            A = (1620, 791)
            B = (1654, 826)
            C = (1591, 820)
            D = (1626, 854)
            self.polygon = [(12, 68), (40, 40), (68, 12), (40, -16), (-16, 40)]
            self.polygon = [(point[0] + 1600, point[1] + 800) for point in self.polygon]
            self.goal_line = Line(B,D)

        elif typ == "um":
            self.polygon = [(805, 60), (70, 20)]
            self.goal_line = ((800, 40), (880, 40))

        elif typ == "lm":
            self.polygon = [(805, 800), (70, 20)]
            self.goal_line = ((800, 840), (880, 840))

        # lines defining hole entry
        self.upper_line = Line(A, B)
        self.lower_line = Line(C, D)    

    def collision(self, ball):

        # collision with diagonal line of corner holes
        if self.typ not in ["um", "lm"] and not ball.holed:
            if self.lower_line.is_below_line(ball.pos) or self.upper_line.is_above_line(ball.pos):
                # reset position
                #while self.lower_line.is_below_line(ball.pos) or self.upper_line.is_above_line(ball.pos):
                #    ball.pos = ball.pos - ball.v

                #print("upper is above:", self.upper_line.is_above_line(ball.pos))
                #print("lower is below:", self.lower_line.is_below_line(ball.pos))

                P = np.array(self.upper_line.P)
                Q = np.array(self.upper_line.Q)

                tangente = (P - Q)/np.linalg.norm(P - Q)
                normale = np.array([tangente[1], -tangente[0]])

                A = np.vstack((normale, tangente)).T

                # split v into v_n & v_t
                parameter = np.linalg.solve(A, ball.v)
                v_n = normale * parameter[0]
                v_t = tangente * parameter[1]

                v_new = -v_n + v_t

                ball.move(v_new)
            
        # check if ball is "behind" goal line to mark it as holed
        con1 = self.typ in ["ul", "ur"] and self.goal_line.is_above_line(ball.pos)
        con2 = self.typ in ["ll", "lr"] and self.goal_line.is_below_line(ball.pos)
        if con1 or con2:
            ball.holed = True
        
        # check if ball is "behind" goal line to mark it as holed (for middle holes)
        if self.typ in ["lm", "um"]:
            in_area = self.goal_line[0][0] < ball.x < self.goal_line[1][0]  # lines are horizontal, so cant use "Line"-class here
            con1 = self.typ in ["lm"] and in_area and ball.y > self.goal_line[1][1]
            con2 = self.typ in ["um"] and in_area and ball.y < self.goal_line[1][1]
            if con1 or con2:
                ball.holed = True

    def draw(self):
        pygame.draw.circle(self.screen, black, self.pos, self.radius)
        if self.typ in ["um", "lm"]:
            pygame.draw.rect(self.screen, green, self.polygon)
        else:
            pygame.draw.polygon(self.screen, black, self.polygon)
        
        # self.upper_line.draw(self.screen)  # red lines
        # self.lower_line.draw(self.screen)


class Line:
    """Helper class to do collisions with diagonal lines of corner holes"""

    def __init__(self, P, Q):
        self.P = P
        self.Q = Q
        self.f_x = Line.compute_line(P, Q)

    @staticmethod
    def compute_line(P, Q):
        a = np.array([[P[0], 1], [Q[0], 1]])
        b = np.array([P[1], Q[1]])
        slope, c = np.linalg.solve(a, b)
        f = lambda x: slope*x + c
        return f

    def is_above_line(self, point):
        in_x_area = min(self.P[0], self.Q[0]) < point[0] < max(self.P[0], self.Q[0])
        in_y_area = min(self.P[1], self.Q[1]) < point[1] < max(self.P[1], self.Q[1])
        if in_x_area and in_y_area:
            return point[1] < self.f_x(point[0])  # sign reverted because Y starts in upper left corner
        else:
            return False

    def is_below_line(self, point):
        in_x_area = min(self.P[0], self.Q[0]) < point[0] < max(self.P[0], self.Q[0])
        in_y_area = min(self.P[1], self.Q[1]) < point[1] < max(self.P[1], self.Q[1])
        if in_x_area and in_y_area:
            return point[1] > self.f_x(point[0])  # sign reverted because Y starts in upper left corner
        else:
            return False
    def draw(self, screen):
        pygame.draw.line(screen, red, self.P, self.Q, 2)


class Queue:

    def __init__(self, screen):
        self.screen = screen

        #drawing polygon
        self.edges = [np.array((30, 31)), np.array((30, 39)), np.array((200, 36)), np.array((200, 34))]
        self.pivot = np.array([0, 35])

        # Rotation matrix, initial values
        self.theda = 15
        scale = self.theda / 1000
        self.rot = np.array(((np.cos(scale), -np.sin(scale)), (np.sin(scale), np.cos(scale))))

    def update(self, pos):
        pass

    def draw(self, ball_pos):
        translation = self.edges + ball_pos - self.pivot
        pygame.draw.polygon(self.screen, grey, translation)

    def rotate(self, rot_speed, elapsed_time):
        if rot_speed != self.theda:
            self.update_rot_mat(rot_speed)

        # translate to origin, rotate, translate back
        for ms in range(0, elapsed_time):  # for equal speed on diff. machines
            self.edges = self.edges - self.pivot
            new_edges = []
            for point in self.edges:
                new_edges.append(np.dot(self.rot, point))
            self.edges = new_edges + self.pivot

    def get_r(self):
        r = self.edges[3] - np.array([0, 34])
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
