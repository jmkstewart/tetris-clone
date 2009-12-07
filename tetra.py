import random

import pygame

from box import *

class Tetra(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.CreateBoxes() # Create 4 new blocks in one of the 4 set formats
        
    def CreateBoxes(self):
        self.box_type = random.randint(1,7)

        if self.box_type == 1:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([1, 0]), Box([2, 0])]
        elif self.box_type == 2:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([0, -1]), Box([0, 1])]
        elif self.box_type == 3:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([1, 0]), Box([1, -1])]
        elif self.box_type == 4:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([1, 0]), Box([1, 1])]
        elif self.box_type == 5:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([0, -1]), Box([1, -1])]
        elif self.box_type == 6:
            self.Boxes = [Box([-1, 0]), Box([-1, 1]), Box([0, 0]), Box([0, 1])]
        else:
            self.Boxes = [Box([-1, 0]), Box([0, 0]), Box([0, 1]), Box([1, 1])]

    def Draw(self, screen, position):
        map(lambda box: box.Draw(screen, position), self.Boxes)


    """Position functions"""
    def GetBoxPositions(self):
        return map(lambda box: box.relative_position, self.Boxes)
    
    def GetLargestVerticalOffset(self):
        return max(map(lambda box: box.GetVerticalOffset(), self.Boxes))

    def GetLeftmostOffset(self):
        return min(map(lambda box: box.relative_position[1], self.Boxes))

    def GetRightmostOffset(self):
        return max(map(lambda box: box.relative_position[1], self.Boxes))

    def GetRect(self):
        top = 0
        left = 0
        width = self.GetRightmostOffset() - self.GetLeftmostOffset() + 1
        height = self.GetLargestVerticalOffset() + 2
        return pygame.Rect(left * 30, top * 30, width * 30, height * 30)
    

    """Turn functions"""
    def ProposedTurnPositions(self):
        return map(lambda box: [box.relative_position[1], box.relative_position[0] * -1], self.Boxes)
    
    def Turn(self):
        # i guess we have to do it on a case by case basis, at least for the square
        if self.box_type != 6:
            
            # take what's in the x position and put it in the y
            # take what's in the y position, negate it, and put it in the x

            # the middle one never changes, do it for fun i guessp
            for box in self.Boxes:
                y = box.relative_position[0]
                box.relative_position[0] = box.relative_position[1]
                box.relative_position[1] = y * -1


    """Update functions"""


    #def Update(self):
