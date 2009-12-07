import pygame

class Preview(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([120, 160])
        self.image.fill([0, 0, 153])

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.preview_sprite = pygame.sprite.RenderPlain((self))

    def Draw(self, screen):
        self.preview_sprite.draw(screen)

        # centre the tetra in the preview frame
        x = (self.rect.centerx - 15) + (self.tetra.GetLeftmostOffset() * -15) + (self.tetra.GetRightmostOffset() * -15)
        y = (self.rect.centery - 15) + 15 + (self.tetra.GetLargestVerticalOffset() * -15)

        self.tetra.Draw(screen, [y, x])
