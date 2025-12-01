import math
import heapq

from board import Board

# This function might be moved to board.py later
def get_neighbors(board: Board, current: tuple[int, int]) -> list[tuple[int, int]]:
    neighbors = []

    x, y = current
    size = board.size
    cell = board.grid[y][x]

    # Up
    if y > 0 and not cell.collide_up:
        neighbor_cell = board.grid[y - 1][x]
        # Check reciprocal collision
        if not neighbor_cell.collide_down:
            neighbors.append((x, y - 1))
    # Down
    if y < size - 1 and not cell.collide_down:
        neighbor_cell = board.grid[y + 1][x]
        # Check reciprocal collision
        if not neighbor_cell.collide_up:
            neighbors.append((x, y + 1))
    # Left
    if x > 0 and not cell.collide_left:
        neighbor_cell = board.grid[y][x - 1]
        # Check reciprocal collision
        if not neighbor_cell.collide_right:
            neighbors.append((x - 1, y))
    # Right
    if x < size - 1 and not cell.collide_right:
        neighbor_cell = board.grid[y][x + 1]
        # Check reciprocal collision
        if not neighbor_cell.collide_left:
            neighbors.append((x + 1, y))

    return neighbors # List of near coordinates that can be reached from current

def reconstruct_path(closed: dict, current: tuple[int, int]) -> list[tuple[int, int]]:
    total_path = [current]

    while current in closed:
        current = closed[current]
        total_path.append(current)

    # NOTE: The path is from dest to src, so needs to be reversed if printed
    #       but is fine when used to move step by step

    return total_path

def heuristic(a: list[int], b: list[int]) -> int:
    # Distance of norm 1 on IR² -> d1(U,V) = |Ux - Vx| + |Uy - Vy|
    # * Positivity: d1(U,V) = 0 iff U = V
    # * Symmetry: d1(U,V) = d1(V,U)
    # * Triangle inequality: d1(U,W) <= d1(U,V) + d1(V,W)
    # Used because only 4 directions are allowed
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(board: Board, src: list[int], dest: list[int]) -> list[tuple[int, int]]:
    size = board.size

    # Open list used as a priority queue
    open_list = []
    heapq.heappush(open_list, (0, tuple(src)))

    # Dictionary of navigated nodes
    closed_set = {}

    # Dictionary for the cost of a node
    g_score = { (x, y): math.inf for x in range(size) for y in range(size) }
    g_score[tuple(src)] = 0

    # Dictionary for the total estimated cost of a node (f = g + h)
    f_score = { (x, y): math.inf for x in range(size) for y in range(size) }
    f_score[tuple(src)] = heuristic(src, dest)

    # While there are still nodes to explore
    while open_list:
        current = heapq.heappop(open_list)[1]

        # Goal is reached
        if current == tuple(dest):
            return reconstruct_path(closed_set, current)
            
        # Get reachable neighbors
        neighbors = get_neighbors(board, current)

        # Explore each neighbor and find the lowest cost path
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1

            # If the best path has been found
            if tentative_g_score < g_score[neighbor]:
                closed_set[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(list(neighbor), dest)

                # Add neighbor to open list if not already present
                if neighbor not in [i[1] for i in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return []  # No path found