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

        self.value = 0                      # Pawn ID (0 = empty, 1-4 = pawn)
        self.is_goal = is_goal
        self.goal_pawn_id = goal_pawn_id

        if is_goal and goal_pawn_id == 0:
            self.goal_pawn_id = 1              # FIXME: redundant with goal_pawn_id?
            # Which pawn this goal is for (0 = no goal, 1-3 = pawn)
        self.collide_left = collide_left
        self.collide_right = collide_right
        self.collide_up = collide_up
        self.collide_down = collide_down

    def draw(self, window: pg.Surface, x: int, y: int) -> None:
        # Cell size in pixels
        size : int = c.CELL_SIZE
        center_x = int(round(size * (x + 0.5)))
        center_y = int(round(size * (y + 0.5)))

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
            pawn_size = size // 2

            pg.draw.circle(window, c.BLACK, (center_x, center_y), pawn_size)
            pg.draw.circle(window, col, (center_x, center_y), pawn_size - 1)
        
        # Draw cross of the pawn color if it's a goal
        if self.is_goal and self.goal_pawn_id > 0:
            # Draw pawn colored cross
            cross_size = size // 3

            cross_color : tuple[int, int, int] = c.PAWN_COLORS[self.goal_pawn_id]

            pg.draw.line(window, c.BLACK, (center_x - cross_size, center_y), (center_x + cross_size, center_y), 4)
            pg.draw.line(window, c.BLACK, (center_x, center_y - cross_size), (center_x, center_y + cross_size), 4)

            pg.draw.line(window, cross_color, (center_x - cross_size + 1, center_y), (center_x + cross_size - 1, center_y), 2)
            pg.draw.line(window, cross_color, (center_x, center_y - cross_size + 1), (center_x, center_y + cross_size - 1), 2)

class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = []
        self.initial_state = []

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

    def clear_pawns(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].value = 0

    def clear_goal(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].is_goal = False
                self.grid[y][x].goal_pawn_id = 0

    def get_goal(self) -> tuple[int,int]:
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x].is_goal:
                    return (x, y)
        return -1

    def set_goal(self, x: int, y: int, pawn_id: int) -> None:
        self.grid[y][x].is_goal = True
        self.grid[y][x].goal_pawn_id = pawn_id

    def set_cell_value(self, x: int, y: int, val: int) -> None:
        self.grid[y][x].value = val
    
    def get_pawn_position(self, pawn_id: int) -> tuple[int,int]:
        # Search the grid for the pawn
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x].value == pawn_id:
                    return (x, y)
        
        # Pawn not found
        return (-1, -1)
    
    def set_pawn_position(self, destination: tuple[int,int], pawn_id: int) -> None:
        # Unpack destination
        x, y = destination
        
        # Validate coordinates
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print(f"Warning: Attempted to set pawn position to invalid coordinates ({x}, {y})")
            return
            
        # Avoids duplicating pawns
        curr_x, curr_y = self.get_pawn_position(pawn_id)
        self.grid[y][x].value = pawn_id
        self.grid[curr_y][curr_x].value = 0

    def move_pawn(self, direction: int, pawn_id: int) -> bool:
        # Get current position
        pos = self.get_pawn_position(pawn_id)
        next_cell = self.get_neighbor(pos, direction)
        
        # No valid move in given direction
        if next_cell == (-1, -1):
            return False
        
        # Move pawn to the furthest possible cell in the given direction
        tmp = pos
        while next_cell != (-1, -1):
            tmp = next_cell
            next_cell = self.get_neighbor(next_cell, direction)
        
        # Update pawn position if it has changed
        if tmp != pos:
            self.set_pawn_position(tmp, pawn_id)
            return True
        
        # Pawn did not move
        return False
        
    def save_initial_state(self) -> None:
        self.initial_state = []

        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = self.grid[y][x]
            
                tmp : tuple[bool, int, int] = (cell.is_goal, cell.goal_pawn_id, cell.value)
                row.append(tmp)
            self.initial_state.append(row)
            
    def load_initial_state(self) -> None:
        if not self.initial_state:
            print("Warning: No initial state saved")
            return
        
        # Restore grid to initial state
        for y in range(self.size):
            for x in range(self.size):
                cell = self.grid[y][x]

                is_goal, goal_pawn_id, value = self.initial_state[y][x]
                
                cell.is_goal = is_goal
                cell.goal_pawn_id = goal_pawn_id
                cell.value = value
                
    
    # TODO: See duplicate usage in astar.py and decide which version to keep
    def get_neighbor(self, current: tuple[int, int], direction: int, pawn_id: int = None) -> tuple[int,int]:
        # Unpack current position
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
        
        # No valid neighbor
        return (-1, -1)

    def draw(self, window: pg.Surface) -> None:
        # Draw all cells
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].draw(window, x, y)
        self.color_possible_goals(window)

    def color_possible_goals(self, window: pg.Surface) -> None:

        for col_id, col_coords in c.PAWN_GOAL_COORDS.items():
            for coord in col_coords:
                x : int = coord[0]
                y : int = coord[1]

                center_x = int(round(c.CELL_SIZE * (x + 0.5)))
                center_y = int(round(c.CELL_SIZE * (y + 0.5)))

                pg.draw.circle(window, c.PAWN_COLORS[col_id], (center_x, center_y), (c.CELL_SIZE // 2) - 7)
