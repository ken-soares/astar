from random import randint

class Cell:
    def __init__(self, is_goal:  bool,
                       collide_left: bool,
                       collide_right: bool,
                       collide_up: bool,
                       collide_down: bool):

        self.is_goal = is_goal
        self.collide_left = collide_left
        self.collide_right = collide_right
        self.collide_up = collide_up
        self.collide_down = collide_down

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = []

    def create_grid(self):
        l = []
        for i in range(self.size):
            for j in range(self.size):
                l.append(Cell(False, False, False, False, False))
            self.grid.append(l)
            l = []

        x = randint(0, self.size-1)
        y = randint(0, self.size-1)

        self.grid[x][y].is_goal = True

