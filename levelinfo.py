

class LevelInfo:
    def __init__(self):
        self.Reset()

    def LineIncrease(self, increase_by):
        self.score = self.score + increase_by
        self.lines_done_this_level = self.lines_done_this_level + increase_by
        
        if self.lines_done_this_level >= 10:
            self.level = self.level + 1
            self.lines_done_this_level = self.lines_done_this_level - 10

    def GameOver(self):
        self.game_over = True

    def Reset(self):
        self.level = 1
        self.lines_done_this_level = 0
        self.game_over = False
        self.score = 0
        
