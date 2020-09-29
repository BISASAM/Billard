from scenebase import SceneBase
from gamescene import GameScene
from tools import Color
import pygame
import pygame.freetype


class TitleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen
        self.text = pygame.freetype.SysFont("Segoe UI Emoji", 50)
        self.text_small = pygame.freetype.SysFont("Segoe UI Emoji", 30)
    
    def ProcessInput(self, events, pressed_keys, elapsed_time):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene(self.screen, "8ball"))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.SwitchToScene(GameScene(self.screen, "9ball"))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
    
    def Update(self, elapsed_time):
        pass
    
    def Render(self):
        mid, height, step = 650, 150, 80
        
        self.screen.fill(Color.black)

        self.text.render_to(self.screen, (mid - 200, height), "Willkommen daheim Mr. O’Sullivan", Color.white)  # eig ein Snooker Spieler, aber der einzige den ich kenne
        self.text_small.render_to(self.screen, (mid, height + step * 2), "⬅  ➡    Zielen", Color.white)
        self.text_small.render_to(self.screen, (mid, height + step * 3), "⬆  ⬇    genaues Zielen", Color.white)
        self.text_small.render_to(self.screen, (mid, height + step * 4), "SPACE     Laden und Schießen", Color.white)
        self.text_small.render_to(self.screen, (mid, height + step * 6), "ENTER     8-Ball starten", Color.white)
        self.text_small.render_to(self.screen, (mid, height + step * 7), "BACKSPACE     9-Ball starten", Color.white)
        self.text_small.render_to(self.screen, (mid, height + step * 8), "ESC          Spiel beenden", Color.white)
    