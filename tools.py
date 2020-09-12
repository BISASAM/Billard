import random
import pygame
from elements import Ball, Hole
from os.path import join


black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
brown = (102, 64, 0)
green = (0, 153, 0)


class Tools:

    @staticmethod
    def create_balls(screen, typ):
        # create balls
        ball_folder = "rsc/balls/"
        ball_list = []
        if typ == "8ball":
            formation = {"fixed": {0: (420, 440), 8: (1340, 440)},
                         "random": {
                "balls": [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15],
                "available_pos": [(1260, 440), (1300, 420), (1300, 460),
                                  (1340, 400), (1340, 480), (1380, 380),
                                  (1380, 420), (1380, 460), (1380, 500),
                                  (1420, 360), (1420, 400), (1420, 440),
                                  (1420, 480), (1420, 520)]
            }
            }
        elif typ == "9ball":
            formation = {"fixed": {0: (420, 440), 1: ((1260, 440)), 9: (1340, 440)},
                         "random": {
                "balls": [2, 3, 4, 5, 6, 7, 8],
                "available_pos": [(1300, 420), (1300, 460), (1340, 400),
                                  (1340, 480), (1380, 420), (1380, 460),
                                  (1420, 440)]
            }
            }
        else:
            raise ValueError('typ must be \"8ball\" or \"9ball\".')

        for key, pos in formation["fixed"].items():
            ball_list.append(Ball(key, screen, pos, join(ball_folder, str(key)+".png")))

        random.shuffle(formation["random"]["available_pos"])
        for key, pos in zip(formation["random"]["balls"], formation["random"]["available_pos"]):
            ball_list.append(Ball(key, screen, pos, join(ball_folder, str(key)+".png")))

        return ball_list

    @staticmethod
    def create_holes(screen):
        width, height = screen.get_size()
        border_thickness = 40
        types = {"ul": (border_thickness, border_thickness),
                 "um": (width//2, border_thickness),
                 "ur": (width-border_thickness, border_thickness),
                 "ll": (border_thickness, height-border_thickness),
                 "lm": (width//2, height-border_thickness),
                 "lr": (width-border_thickness, height-border_thickness)}
        hole_list = []
        for typ in types:
            hole_list.append(Hole(screen, types[typ], 40, typ))

        return hole_list

    @staticmethod
    def draw_table(screen):

        size = width, height = 1680, 880
        border_thickness = 40
        border_koord = [(0, 0, width, border_thickness), (0, height-border_thickness, width, border_thickness),
                        (0, 0, border_thickness, height),  (width-border_thickness, 0, border_thickness, height)]

        # borders
        for koord in border_koord:
            pygame.draw.rect(screen, brown, koord)

    @staticmethod
    def jederMitJedem(liste):
        result = []
        start = 0
        for entry in liste:
            start += 1
            for i in range(start, len(liste)):
                result.append((entry, liste[i]))
        return result
