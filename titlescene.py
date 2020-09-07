from scenebase import SceneBase
from gamescene import GameScene
import pygame


class TitleScene(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        self.screen = screen
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene(self.screen))
    
    def Update(self, elapsed_time):
        pass
    
    def Render(self):
        # For the sake of brevity, the title scene is a blank red screen
        self.screen.fill((255, 0, 0))