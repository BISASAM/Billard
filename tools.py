import random
import pygame
import math
from elements import Ball, Hole
from os.path import join
import numpy as np


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
            hole_list.append(Hole(screen, types[typ], typ))

        return hole_list

    @staticmethod
    def draw_table(screen):

        size = width, height = 1680, 880
        border_thickness = 40
        border_koord = [(0, 0, width, border_thickness), (0, height-border_thickness, width, border_thickness),
                        (0, 0, border_thickness, height),  (width-border_thickness, 0, border_thickness, height)]

        screen.fill(Color.green)
        for koord in border_koord:
            pygame.draw.rect(screen, Color.brown, koord)

    @staticmethod
    def jederMitJedem(liste):
        #  TODO: use python collections module here
        result = []
        start = 0
        for entry in liste:
            start += 1
            for i in range(start, len(liste)):
                result.append((entry, liste[i]))
        return result

    @staticmethod
    def find_free_pos(balls, width=1680, height=880):
        #  Archimedische Spirale um (start) herum bis was frei ist.
        #  x=r(p)cos(p), y=r(p)sin(p), r(p)=ap

        start = (420, 440)  # Anfangsposition der weißen Kugel
        a = 40/(2*math.pi)  # Abstand der spiralarme ist ball durchmesser
        r = lambda x: a*x
        x = lambda p: int( r(p)*math.cos(p) ) + start[0]
        y = lambda p: int( r(p)*math.sin(p) ) + start[1]

        for p in np.arange(0, 12*math.pi, math.pi/12):  # 6 Umdrehungen
            X, Y = x(p), y(p)
            in_table_range = 60 < X < width-60 and 60 < Y < height-60
            if in_table_range:
                for ball in balls:  # check if new position collides with any ball on table 
                    if np.linalg.norm(np.array((X,Y)) - ball.pos) < 40:
                        break
                else:
                    return np.array((X, Y))
        else:
            raise("Pech gehabt, kein Platz gefunden")
    
    @staticmethod
    def arrow(screen, pos):
        #  little arrow that points to pos
        #  helpful for development
        arrow = [(0, 0), (20, 0), (20, 10)]
        arrow = [(point[0]+pos[0], point[1]+pos[1]) for point in arrow]
        pygame.draw.polygon(screen, Color.red, arrow)


class Color:

    black = (0, 0, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    brown = (102, 64, 0)
    green = (0, 153, 0)



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    points = [[1380,  460], [1381,  460],[1382,  461],[1383,  463],[1383,  465],[1382,  468],[1380,  470],[1377,  471],[1374,  471],[1370,  470],[1366,  468],[1363,  464],
            [1360,  460],[1360,  455],[1360,  449],[1363,  443],[1367,  437],[1373,  433],[1380,  430],[1388,  430],[1396,  432],[1404,  436],[1411,  442],[1417,  451],
            [1420,  460],[1420,  470],[1417,  481],[1411,  491],[1403,  500],[1392,  506],[1380,  510],[1367,  509],[1354,  506],[1342,  498],[1331,  488],[1324,  475],
            [1320,  460],[1321,  445],[1326,  429],[1335,  415],[1347,  403],[1363,  394],[1380,  390],[1398,  391],[1416,  397],[1433,  407],[1446,  422],[1455,  440],[1460,  460]]
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    plt.scatter(x, y)
    plt.show()



