import pygame

from font import *
from button import *

class DisplayInfo(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([120, 160])
        self.image.fill([0, 0, 153])

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.display_info_sprite = pygame.sprite.RenderPlain((self))

        self.CreateNewGameButton()


    def Draw(self, screen):
        self.display_info_sprite.draw(screen)

        self.new_game_button.Draw(screen)
        self.level_text.Draw(screen)
        self.score_text.Draw(screen)


    def AddRestartListener(self, hook):
        self.new_game_button.AddButtonListener(hook)


    def Event(self, event):
        self.new_game_button.Event(event)


    def CreateNewGameButton(self):
        self.new_game_button = Button(self.rect.move(0, -40), "Restart")
        self.new_game_button.Show()

    def SetLevel(self, level):
        self.level_text = Font(self.rect, "Level:  " + str(level))
        self.level_text.Show()

    def SetScore(self, score):
        self.score_text = Font(self.rect.move(0, 40), "Score:  " + str(score))
        self.score_text.Show()
