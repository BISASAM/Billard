from scenebase import SceneBase
from gamescene import GameScene
import pygame
import pygame.freetype


black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
brown = (102, 64, 0)
green = (0, 153, 0)

class TitleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen
        self.text = pygame.freetype.SysFont("Segoe UI Emoji", 50)
        self.text_small = pygame.freetype.SysFont("Segoe UI Emoji", 30)
    
    def ProcessInput(self, events, pressed_keys, elapsed_time):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene(self.screen))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
    
    def Update(self, elapsed_time):
        pass
    
    def Render(self):
        # For the sake of brevity, the title scene is a blank red screen
        mid, heigt, step = 650, 200, 80
        
        self.screen.fill(black)

        self.text.render_to(self.screen, (mid - 200, heigt), "Willkommen Daheim Mr. O’Sullivan", white)  # eig ein Snooker Spieler, aber der einzige den ich kenne
        self.text_small.render_to(self.screen, (mid, heigt + step * 2), "⬅  ➡    Zielen", white)
        self.text_small.render_to(self.screen, (mid, heigt + step * 3), "⬆  ⬇    genaues Zielen", white)
        self.text_small.render_to(self.screen, (mid, heigt + step * 4), "SPACE     Laden und Schießen", white)
        self.text_small.render_to(self.screen, (mid, heigt + step * 6), "ENTER     Spiel starten", white)
        self.text_small.render_to(self.screen, (mid, heigt + step * 7), "ESC          Spiel beenden", white)
    