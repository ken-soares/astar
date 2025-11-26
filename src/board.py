import pygame as pg

import consts as c

# Maybe move this in another file like cell.py
class Cell:
    def __init__(self, is_goal:  bool,
                       collide_left: bool,
                       collide_right: bool,
                       collide_up: bool,
                       collide_down: bool):

        self.value = 0  # TODO: May be changed in the future as it is ugly
        self.is_goal = is_goal
        self.collide_left = collide_left
        self.collide_right = collide_right
        self.collide_up = collide_up
        self.collide_down = collide_down

    def draw(self, window: pg.Surface, x: int, y: int) -> None:
        size : int = c.CELL_SIZE

        left : bool = self.collide_left
        right : bool = self.collide_right
        up : bool = self.collide_up
        down : bool = self.collide_down

        # TODO: Change color depending on value
        col : tuple[int, int, int] = c.WHITE
        if self.is_goal:
            col = c.RED
        if self.value > 0:
            col = c.GREEN

        pg.draw.rect(window, c.BLACK, (x * size, y * size, size, size))

        pg.draw.rect(window, col, (x * size + 1 + 2 * left, y * size + 1 + 2 * up, size - 1 - 2 * right, size - 1 - 2 * down))

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = []

    def create_grid(self, filename: str) -> None:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                row = []
                values = line.strip().split(',')
                for value in values:
                    collision = int(value)
                    collide_left = bool(collision & c.COL_LEFT)
                    collide_right = bool(collision & c.COL_RIGHT)
                    collide_up = bool(collision & c.COL_UP)
                    collide_down = bool(collision & c.COL_DOWN)
                    
                    cell = Cell(False, collide_left, collide_right, collide_up, collide_down)
                    row.append(cell)
                self.grid.append(row)
        except IOError:
            print("Error: File not found.")

    def clear_grid(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].value = 0

    def clear_goal(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].is_goal = False

    def set_goal(self, x: int, y: int) -> None:
        self.grid[y][x].is_goal = True

    def set_cell_value(self, x: int, y: int, val: int) -> None:
        self.grid[y][x].value = val

    def draw(self, window: pg.Surface) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].draw(window, x, y)
