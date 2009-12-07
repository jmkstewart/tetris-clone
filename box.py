import pygame

class Box(pygame.sprite.Sprite):
    size = 30
    draw_size = 28

    relative_min_width = 0
    relative_max_width = 12
    
    def __init__(self, initial_position):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.Surface([self.draw_size, self.draw_size])
        self.image.fill([153, 0, 0])

        self.relative_position = initial_position
        
        self.box_sprite = pygame.sprite.RenderPlain((self))

    def Draw(self, screen, position):
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = position[0] + (self.relative_position[0] * self.size) + 1
        self.rect.left = position[1] + (self.relative_position[1] * self.size) + 1

        #print "Box rect.top = " + str(self.rect.top)
        #print "Box rect.left = " + str(self.rect.left)

        self.box_sprite.draw(screen)


    """Position Functions"""
    def GetVerticalOffset(self):
        return self.relative_position[0]

    def GetHorizontalOffset(self):
        return self.relative_position[1]
    

    """Update functions"""
    #def Update(self):
