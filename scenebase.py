class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys, elapsed_time):
        print("needs to be overwritten")

    def Update(self, elapsed_time):
        print("needs to be overwritten")

    def Render(self):
        print("needs to be overwritten")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)