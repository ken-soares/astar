from random import randint

import pygame as pg

import consts as c
from cell import Cell

class Board:
    def __init__(self, size: int):
        self.size : int = size
        self.grid : list = []
        self.initial_state : list = []
        self.goal : tuple[int,int] = (-1, -1)

    def create_grid(self, filename : str) -> None:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Parse each line into cells
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

            # Set goal pawn ids in cells
            for col_id, col_coords in c.PAWN_GOAL_COORDS.items():
                for coord in col_coords:
                    x : int = coord[0]
                    y : int = coord[1]

                    self.grid[y][x].goal_pawn_id = col_id
        except IOError:
            print("Error: File not found.")

    def clear(self) -> None:
        self.clear_pawns()
        self.clear_goal()
    
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

    def init_pawns(self) -> None:
        pawns_coords : list = self.generate_unique_coordinates()

        for i in range(c.PAWN_NUMBER):
            tmp_x, tmp_y = pawns_coords[i]
            self.set_cell_value(tmp_x, tmp_y, i + 1)


    def choose_goal(self) -> None:
        goal_pawn_id : int = randint(1, c.PAWN_NUMBER)
        tmp_len : int = len(c.PAWN_GOAL_COORDS[goal_pawn_id])
        goal_coords_id : int = randint(0, tmp_len - 1)

        goal_x, goal_y = c.PAWN_GOAL_COORDS[goal_pawn_id][goal_coords_id]

        self.set_as_goal(goal_x, goal_y)

    def generate_unique_coordinates(self) -> list:
        # Initial coordinates list for pawns
        coordinates : list = []

        # Center of the board is non valid
        illegal_coords : list = [(7,7), (7,8), (8,7), (8,8)]

        # Add goal coordinates to illegal coords
        for _, tuples in c.PAWN_GOAL_COORDS.items():
            for c1, c2 in tuples:
                illegal_coords.append((c1, c2))

        # Generate unique coordinates for each pawn
        while len(coordinates) < c.PAWN_NUMBER:
            x : int = randint(0, self.size - 1)
            y : int = randint(0, self.size - 1)
            coord = (x, y)

            if coord not in illegal_coords:
                coordinates.append(coord)
        
        return coordinates

    def get_goal_color(self) -> int:
        x, y = self.goal
        if (x == -1 or y == -1):
            return 0
        
        return self.grid[y][x].goal_pawn_id

    def get_goal(self) -> tuple[int,int]:
        return self.goal

    def set_as_goal(self, x : int, y : int) -> None:
        t_x, t_y = self.goal
        if (t_x != -1 and t_y != -1):
            self.grid[t_y][t_x].is_goal = False

        self.goal = (x, y)
        self.grid[y][x].is_goal = True

    def clear_goal(self) -> None:
        x, y = self.goal
        if (x == -1 or y == -1):
            return

        self.grid[y][x].is_goal = False
        self.goal = (-1, -1)

    def set_cell_value(self, x : int, y : int, val : int) -> None:
        self.grid[y][x].value = val
    
    def get_pawn(self, pawn_id : int) -> tuple[int, int]:
        # Search the grid for the pawn
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x].value == pawn_id:
                    return (x, y)
        
        # Pawn not found
        return (-1, -1)
    
    def set_pawn(self, destination : tuple[int, int], pawn_id : int) -> None:
        # Unpack destination
        x, y = destination
        
        # Validate coordinates
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print(f"Warning: Attempted to set pawn position to invalid coordinates ({x}, {y})")
            return
            
        # Avoids duplicating pawns
        curr_x, curr_y = self.get_pawn(pawn_id)
        self.grid[y][x].value = pawn_id
        self.grid[curr_y][curr_x].value = 0

    def clear_pawns(self) -> None:
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].value = 0

    def move_pawn(self, pawn_id : int, direction : int) -> bool:
        # Get current position
        pos = self.get_pawn(pawn_id)
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
            self.set_pawn(tmp, pawn_id)
            return True
        
        # Pawn did not move
        return False

    def simulate_move(self, pos : tuple, direction : int) -> tuple:
        next_cell = self.get_neighbor(pos, direction)
        
        # No valid move in given direction
        if next_cell == (-1, -1):
            return (-1, -1)
        
        # Move pawn to the furthest possible cell in the given direction
        tmp = pos
        while next_cell != (-1, -1):
            tmp = next_cell
            next_cell = self.get_neighbor(next_cell, direction)
        
        # Update pawn position if it has changed
        if tmp != pos:
            return tmp
        
        # Pawn did not move
        return (-1, -1)
    
    def get_neighbor(self, current : tuple[int, int], direction : int) -> tuple[int, int]:
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

    def draw(self, window : pg.Surface) -> None:
        # Draw all cells
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].draw(window, x, y)