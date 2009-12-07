import pygame

class Font:
    def __init__(self, containing_rect, text):
        self.containing_rect = containing_rect

        self.show = False

        self.SetText(text)

    def Draw(self, screen):
        if self.show:
            screen.blit(self.text, self.text_rect)

    def Show(self):
        self.show = True

    def Hide(self):
        self.show = False

    def SetText(self, text):
        font = pygame.font.Font(None, 32)
        
        self.text = font.render(text, True, (255,255, 255))
        
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.containing_rect.centerx
        self.text_rect.centery = self.containing_rect.centery
