import pygame as pg

import consts as c

class Cell:
    def __init__(self, is_goal : bool, goal_pawn_id : int, collide_left : bool, collide_right : bool, collide_up : bool, collide_down : bool):
        # Cell properties
        self.value : int= 0                      # Pawn ID (0 = empty, 1-4 = pawn)
        self.is_goal : bool = is_goal
        self.goal_pawn_id : int = goal_pawn_id # Which pawn this goal is for (0 = no goal, 1-4 = pawn)

        # Failsafe in case of incorrect initialization
        if is_goal and goal_pawn_id == 0:
            self.goal_pawn_id = 1
            
        # Collision flags
        self.collide_left : bool = collide_left
        self.collide_right : bool = collide_right
        self.collide_up : bool = collide_up
        self.collide_down : bool = collide_down

    def draw(self, window : pg.Surface, x : int, y : int) -> None:
        # Cell size in pixels
        size : int = c.CELL_SIZE
        center_x : int = int(round(size * (x + 0.5)))
        center_y : int = int(round(size * (y + 0.5)))

        # Retrieve collision info
        left : bool = self.collide_left
        right : bool = self.collide_right
        up : bool = self.collide_up
        down : bool = self.collide_down

        # Retrieve proper cell/pawn color
        col : tuple[int, int, int] = c.WHITE

        if self.goal_pawn_id > 0:
            col = c.PAWN_COLORS[self.goal_pawn_id]

        # Draw cell
        pg.draw.rect(window, c.BLACK, (x * size, y * size, size, size))
        pg.draw.rect(window, col, (x * size + 1 + 2 * left, y * size + 1 + 2 * up, size - 1 - 2 * right, size - 1 - 2 * down))

        # Draw pawn if present
        if self.value > 0:
            col = c.PAWN_COLORS[self.value]
            pawn_size : int = size // 3

            pg.draw.circle(window, c.BLACK, (center_x, center_y), pawn_size)
            pg.draw.circle(window, c.WHITE, (center_x, center_y), pawn_size - 1)
            pg.draw.circle(window, col, (center_x, center_y), pawn_size - 2)
        
        # Draw cross of the pawn color if it's a goal
        if self.is_goal and self.goal_pawn_id > 0:
            # Draw pawn colored cross
            cross_size : int = size // 3

            pg.draw.line(window, c.BLACK, (center_x - cross_size, center_y), (center_x + cross_size, center_y), 4)
            pg.draw.line(window, c.BLACK, (center_x, center_y - cross_size), (center_x, center_y + cross_size), 4)

            pg.draw.line(window, c.WHITE, (center_x - cross_size + 1, center_y), (center_x + cross_size - 1, center_y), 2)
            pg.draw.line(window, c.WHITE, (center_x, center_y - cross_size + 1), (center_x, center_y + cross_size - 1), 2)