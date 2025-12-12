import pygame as pg

import consts as c

# Maybe move this in another file like cell.py
class Cell:
    def __init__(self, is_goal:  bool,
                       goal_pawn_id: int,
                       collide_left: bool,
                       collide_right: bool,
                       collide_up: bool,
                       collide_down: bool):

        self.value = 0  # TODO: May be changed in the future as it is ugly
        self.is_goal = is_goal
        self.goal_pawn_id = goal_pawn_id  # Which pawn this goal is for (0 = no goal, 1-3 = pawn)
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
        if self.value == 1 or self.goal_pawn_id == 1:
            col = c.GREEN
        elif self.value == 2 or self.goal_pawn_id == 2:
            col = c.BLUE
        elif self.value == 3 or self.goal_pawn_id == 3:
            col = c.FUCHSIA

        pg.draw.rect(window, c.BLACK, (x * size, y * size, size, size))

        pg.draw.rect(window, col, (x * size + 1 + 2 * left, y * size + 1 + 2 * up, size - 1 - 2 * right, size - 1 - 2 * down))
        
        # Draw red cross if it's a goal
        if self.is_goal and self.goal_pawn_id > 0:
            # Draw red cross
            cross_color = c.RED
            center_x = x * size + size // 2
            center_y = y * size + size // 2
            cross_size = size // 3
            
            # Horizontal line of cross
            pg.draw.line(window, cross_color, 
                        (center_x - cross_size, center_y),
                        (center_x + cross_size, center_y), 3)
            
            # Vertical line of cross
            pg.draw.line(window, cross_color,
                        (center_x, center_y - cross_size),
                        (center_x, center_y + cross_size), 3)

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = []
        self.initial_state = None
        self.pawn_colors = ["Green", "Blue", "Fuchsia"]

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
                    
                    cell = Cell(False, 0, collide_left, collide_right, collide_up, collide_down)
                    row.append(cell)
                self.grid.append(row)
        except IOError:
            print("Error: File not found.")
            
    def get_pawn_colors(self):
        return self.pawn_colors

    def clear_grid(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].value = 0

    def clear_goal(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].is_goal = False
                self.grid[y][x].goal_pawn_id = 0

    def set_goal(self, x: int, y: int, pawn_id: int) -> None:
        self.grid[y][x].is_goal = True
        self.grid[y][x].goal_pawn_id = pawn_id

    def set_cell_value(self, x: int, y: int, val: int) -> None:
        self.grid[y][x].value = val
        
    def move_pawn(self, direction: int, pawn_id: int) -> bool:
        pos = self.get_pawn_position(pawn_id)
        next_cell = self.get_neighbor(pos, direction)
        
        if next_cell == (-1, -1):
            return False
        
        tmp = pos
        while next_cell != (-1, -1):
            tmp = next_cell
            next_cell = self.get_neighbor(next_cell, direction)
        
        if tmp != pos:
            self.set_pawn_position(tmp, pawn_id)
            return True
        
        return False
        
    def save_initial_state(self) -> None:
        self.initial_state = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = self.grid[y][x]
                new_cell = Cell(
                    cell.is_goal,
                    cell.goal_pawn_id,
                    cell.collide_left,
                    cell.collide_right,
                    cell.collide_up,
                    cell.collide_down
                )
                new_cell.value = cell.value
                row.append(new_cell)
            self.initial_state.append(row)
            
    def reset_to_initial(self) -> None:
        if self.initial_state is None:
            print("Warning: No initial state saved")
            return
        
        self.grid = []
        
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = self.initial_state[y][x]
                new_cell = Cell(
                    cell.is_goal,
                    cell.goal_pawn_id,
                    cell.collide_left,
                    cell.collide_right,
                    cell.collide_up,
                    cell.collide_down
                )
                new_cell.value = cell.value  # Restore pawn value
                row.append(new_cell)
            self.grid.append(row)

    def set_pawn_position(self, destination: tuple[int,int], pawn_id: int) -> None:
        x, y = destination
        
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print(f"Warning: Attempted to set pawn position to invalid coordinates ({x}, {y})")
            return
            
        curr_x, curr_y = self.get_pawn_position(pawn_id)
        self.grid[y][x].value = pawn_id
        self.grid[curr_y][curr_x].value = 0
    
    # TODO: See duplicate usage in astar.py and decide which version to keep
    def get_neighbor(self, current: tuple[int, int], direction: int, pawn_id: int = None) -> tuple[int,int]:
        x, y = current
        size = self.size
        cell = self.grid[y][x]

        # Up
        if direction == c.MOVE_UP:
            if y > 0 and not cell.collide_up:
                neighbor_cell = self.grid[y - 1][x]
                if not neighbor_cell.collide_down and neighbor_cell.value == 0:
                    return (x, y - 1)

        # Down
        if direction == c.MOVE_DOWN:
            if y < size - 1 and not cell.collide_down:
                neighbor_cell = self.grid[y + 1][x]
                if not neighbor_cell.collide_up and neighbor_cell.value == 0:
                    return (x, y + 1)
                    
        # Left
        if direction == c.MOVE_LEFT:
            if x > 0 and not cell.collide_left:
                neighbor_cell = self.grid[y][x - 1]
                if not neighbor_cell.collide_right and neighbor_cell.value == 0:
                    return (x - 1, y)
                    
        # Right
        if direction == c.MOVE_RIGHT:
            if x < size - 1 and not cell.collide_right:
                neighbor_cell = self.grid[y][x + 1]
                if not neighbor_cell.collide_left and neighbor_cell.value == 0:
                    return (x + 1, y)
        
        return (-1,-1)

    def get_pawn_position(self, pawn_id: int) -> tuple[int,int]:
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x].value == pawn_id:
                    return (x,y)

    def draw(self, window: pg.Surface) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].draw(window, x, y)
