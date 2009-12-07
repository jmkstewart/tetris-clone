import sys

import pygame

import grid
import levelinfo
import preview
import displayinfo

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=480, height=500):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))


    """This is the Main Loop of the Game"""
    def MainLoop(self):
        self.LoadComponents()
        
        while True:
            self.HandleEvents()
            
            self.Update()

            self.Draw()
        
    def LoadComponents(self):
        self.level_info = levelinfo.LevelInfo()
        self.preview = preview.Preview([320, 40])
        self.display_info = displayinfo.DisplayInfo([320, 300])
        self.grid = grid.Grid([40, 40], self.level_info.LineIncrease, self.level_info.Reset, self.level_info.GameOver, self.preview)
        self.display_info.AddRestartListener(self.grid.Restart)

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            else:
                self.FireEvent(event)
    
    def Update(self):
        self.display_info.SetLevel(self.level_info.level)
        self.display_info.SetScore(self.level_info.score)
        
        self.grid.SetLevel(self.level_info.level)
        self.grid.Update()
        
        pygame.display.update()

    def Draw(self):
        self.preview.Draw(self.screen)
        self.display_info.Draw(self.screen)
        self.grid.Draw(self.screen)
        
        pygame.display.flip()


    def FireEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE, pygame.K_p]:
                self.grid.Event(event)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            self.display_info.Event(event)
        

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
