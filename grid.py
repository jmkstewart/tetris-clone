import pygame

from tetra import *
from staticbox import *
from font import *

class Grid(pygame.sprite.Sprite):    
    def __init__(self, initial_position, line_inc_hook, reset_hook, hit_top_hook, preview):
        pygame.sprite.Sprite.__init__(self)

        random.seed()

        self.image = pygame.Surface([240, 420])
        self.image.fill([0, 0, 153])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

        self.line_inc_hook = line_inc_hook
        self.reset_hook = reset_hook
        self.hit_top_hook = hit_top_hook
        self.preview = preview

        self.grid_leftside = 0
        self.grid_width = 8
        self.grid_height = 14

        self.pause_text = Font(self.rect, "Paused")
        self.game_over_text = Font(self.rect, "Game Over!")

        self.grid_sprite = pygame.sprite.RenderPlain((self))

        self.InitGame()

    def Restart(self):
        self.pause_text.Hide()
        self.game_over_text.Hide()

        self.reset_hook()
        
        self.InitGame()

    def InitGame(self):
        self.ticks_between_lower = 1000
        self.paused = False
        self.game_over = False

        self.static_boxes = [[0 for col in range(self.grid_width)] for row in range(self.grid_height)]

        self.preview.tetra = Tetra()
        self.CreateNewTetra()

        self.Start()

    def CreateNewTetra(self):
        self.tetra = self.preview.tetra
        self.preview.tetra = Tetra()
        
        # pops out a new tetra at the top of the screen
        self.tetra_position = [1, 4]


    """Draw functions"""
    def GetRealPosition(self, grid_position):
        return [(grid_position[0] * 30) + self.rect.top,
                (grid_position[1] * 30) + self.rect.left]

    def MapOverMap(self, fn, double_iterable):
        # for each value in a 2d matrix, execute the fn function
        map(lambda entry: map(fn, entry), double_iterable)

    def Draw(self, screen):
        self.grid_sprite.draw(screen)

        self.tetra.Draw(screen, self.GetRealPosition(self.tetra_position))

        def DrawStaticBox(box):
            if box != 0:
                box.Draw(screen, self.GetRealPosition(box.relative_position))

        self.MapOverMap(DrawStaticBox, self.static_boxes)

        self.pause_text.Draw(screen)
        self.game_over_text.Draw(screen)


    """Tetra update functions"""
    def TurnTetra(self):
        proposed = self.tetra.ProposedTurnPositions()
        if (not self.TetraWillHitStaticPosition(proposed, [0, 0])) and (not self.TetraWillHitWalls(proposed, [0, 0])):
            self.tetra.Turn()
        
    def MoveTetraLeft(self):
        if (self.tetra_position[1] + self.tetra.GetLeftmostOffset() > self.grid_leftside) and not self.TetraWillHitStatic([0, -1]):
            self.tetra_position[1] = self.tetra_position[1] - 1

    def MoveTetraRight(self):
        if (self.tetra_position[1] + self.tetra.GetRightmostOffset() < self.grid_leftside + self.grid_width - 1) and not self.TetraWillHitStatic([0, 1]):
            self.tetra_position[1] = self.tetra_position[1] + 1

    def MoveTetraDown(self):
        if self.tetra_position[0] + self.tetra.GetLargestVerticalOffset() >= self.grid_height - 1 or self.TetraWillHitStatic([1, 0]):
            self.StopTetra()
            return False
        else:
            self.tetra_position[0] = self.tetra_position[0] + 1

        return True

    def MoveTetraToBottom(self):
        tetra_above_bottom = True
        while tetra_above_bottom:
            tetra_above_bottom = self.MoveTetraDown()

    def AddTetraPosition(self, position, change):
        new_position = [0, 0]
        new_position[0] = position[0] + self.tetra_position[0] + change[0]
        new_position[1] = position[1] + self.tetra_position[1] + change[1]
        return new_position

    def TetraWillHitWalls(self, positions, change):
        for position in positions:
            full_pos = self.AddTetraPosition(position, change)
            if (full_pos[1] < self.grid_leftside) or (full_pos[1] > self.grid_leftside + self.grid_width - 1) or (full_pos[0] > self.grid_height - 1) or (full_pos[0] < 0):
                return True
        return False
        
    def TetraWillHitStatic(self, change):
        return self.TetraWillHitStaticPosition(self.tetra.GetBoxPositions(), change)
        
    def TetraWillHitStaticPosition(self, positions, change):
        for position in positions:
            if self.BoxWillHitStatic(self.AddTetraPosition(position, change)):
                return True
        return False

    def BoxWillHitStatic(self, dynamic_position):
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                box = self.static_boxes[row][col]
                #box.relative_position[0] = row and box.relative_position[1] = col
                if box != 0 and row == dynamic_position[0] and col == dynamic_position[1]:
                    return True
        return False


    """Change Tetra functions"""
    def StopTetra(self):
        # get the positions of the boxes in the tetra currently
        positions = self.tetra.GetBoxPositions()
        for position in positions:
            position[0] = position[0] + self.tetra_position[0]
            position[1] = position[1] + self.tetra_position[1]

        # create static boxes in those positions
        for position in positions:
            if self.static_boxes[position[0]][position[1]] != 0:
                self.GameOver()
            else:
                self.static_boxes[position[0]][position[1]] = StaticBox(position)

        self.CreateNewTetra()
                
    def Start(self):
        self.last_lower_time = pygame.time.get_ticks()


    """Event functions"""
    def Event(self, event):
        if not self.game_over:
            if event.key == pygame.K_p:
                self.Pause()

            if not self.paused:
                if(event.key == pygame.K_RIGHT):
                    self.MoveTetraRight()
                elif(event.key == pygame.K_LEFT):
                    self.MoveTetraLeft()
                elif(event.key == pygame.K_DOWN):
                    self.MoveTetraDown()
                elif(event.key == pygame.K_UP):
                    self.TurnTetra()
                elif(event.key == pygame.K_SPACE):
                    self.MoveTetraToBottom()


    """Grid change functions"""
    def SetLevel(self, level):
        self.ticks_between_lower = 1000 * ((2.0 / 3.0) ** level)

    def RemoveRowOfBlocks(self, row_index):
        # for every row above the removing row, move it down
        for row in range(row_index, 0, -1):
            for col in range(0, self.grid_width):
                self.static_boxes[row][col] = self.static_boxes[row - 1][col]
                
                if self.static_boxes[row][col] != 0:
                    self.static_boxes[row][col].IncVerticalOffset()

        # for the top row, 0 it all
        self.static_boxes[0] = [0 for col in range(self.grid_width)]

    def RowsThatAreFull(self):
        ret = []
        for row in range(0, self.grid_height):
            if(reduce(lambda sofar, box: sofar and (box != 0), self.static_boxes[row], True)):
                ret.append(row)
        return ret
    

    """Update functions"""
    def GameOver(self):
        self.game_over = True
        self.hit_top_hook()
        self.game_over_text.Show()

    def Pause(self):
        if self.paused:
            self.Start()
            self.pause_text.Hide()
        else:
            self.pause_text.Show()
            
        self.paused = not self.paused
        
    def Update(self):
        if not self.paused and not self.game_over:
            if (pygame.time.get_ticks() - self.last_lower_time) > self.ticks_between_lower:
                self.MoveTetraDown()
                self.last_lower_time = pygame.time.get_ticks()

            full_rows = self.RowsThatAreFull()
            for row in full_rows:
                self.RemoveRowOfBlocks(row)

            self.line_inc_hook(len(full_rows))

