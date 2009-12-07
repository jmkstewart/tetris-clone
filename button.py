import pygame

from font import *

LEFT = 1

class Button(Font):
    def __init__(self, containing_rect, text):
        Font.__init__(self, containing_rect, text)

        self.button_text = text

        self.listeners = []

    def Draw(self, screen):
        if self.show:
            screen.blit(self.background, self.background_rect.topleft)
        
        Font.Draw(self, screen)


    def AddButtonListener(self, hook):
        self.listeners.append(hook)

    def NotifyListeners(self):
        map(lambda fun: fun(), self.listeners)


    def Event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            self.SetTextWithColour(self.button_text, (0, 80, 153))
            if self.background_rect.collidepoint(event.pos):
                self.NotifyListeners()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            self.SetTextWithColour(self.button_text, (0, 180, 153))


    def SetText(self, text):
        self.SetTextWithColour(text, (0, 80, 153))
            
    def SetTextWithColour(self, text, background_colour):
        font = pygame.font.Font(None, 32)
        
        self.text = font.render(text, True, (255,255, 255), background_colour)
        
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.containing_rect.centerx
        self.text_rect.centery = self.containing_rect.centery

        self.background_rect = self.text_rect.inflate(15, 10)
        self.background = pygame.Surface(self.background_rect.size)
        self.background.fill(background_colour)
        
