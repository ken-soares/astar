import math
import heapq

import consts as c

from board import Board

def get_neighbors(board : Board, state : tuple) -> list[tuple]:
    neighbors : list = []

    # For each pawn, try each possible move
    for pawn_id in range(1, c.PAWN_NUMBER + 1):
        for direction in [c.MOVE_UP, c.MOVE_DOWN, c.MOVE_LEFT, c.MOVE_RIGHT]:
            board.clear_pawns()

            # Set pawns positions according to the current state
            for i in range(c.PAWN_NUMBER):
                x, y = state[i]
                board.set_cell_value(x, y, i + 1)

            if board.move_pawn(pawn_id, direction):
                # If move is successful, record new state
                new_pawns : list = []
                for i in range(c.PAWN_NUMBER):
                    new_pawns.append(board.get_pawn(i + 1))

                neighbors.append(tuple(new_pawns))

    return neighbors

def reconstruct_path(closed : dict, current : tuple) -> list[tuple]:
    total_path = [current]

    while current in closed:
        current = closed[current]
        total_path.append(current)

    # NOTE: The path is from dest to src, so needs to be reversed if printed
    #       but is fine when used to move step by step

    return total_path

def astar(board : Board, h_score : dict, stop_event=None) -> list[tuple]:
    goal_pos : tuple[int, int] = board.get_goal()
    goal_id : int = board.get_goal_color()
    goal_index : int = goal_id - 1

    # Initial state: positions of all pawns (node is a tuple of pawn coords)
    pawns : list = []
    for i in range(c.PAWN_NUMBER):
        pawns.append(board.get_pawn(i + 1))

    state = tuple(pawns)

    # Open list used as a priority queue
    open_list : list = []
    heapq.heappush(open_list, (0, state))

    # Dictionary of navigated nodes
    closed_set : dict = {}

    # Dictionary for the cost of a node (g) and total estimated cost (f)
    g_score : dict = {} # If not in dict, value is infinity
    g_score[state] = 0

    f_score : dict = {}
    f_score[state] = h_score.get(state[goal_index], math.inf)

    # While there are still nodes to explore
    while open_list:
        if stop_event and stop_event.is_set():
            return []
        
        current_state : tuple = heapq.heappop(open_list)[1]

        # Goal is reached when the goal pawn is at the goal position
        if current_state[goal_index] == goal_pos:
            board.load_initial_state()
            return reconstruct_path(closed_set, current_state)
        # Get reachable neighbors
        next_states = get_neighbors(board, current_state)

        # Explore each neighbor and find the lowest cost path
        for ns in next_states:
            tentative_g_score : int = g_score.get(current_state, math.inf) + 1

            # If the best path has been found
            if tentative_g_score < g_score.get(ns, math.inf):
                closed_set[ns] = current_state
                g_score[ns] = tentative_g_score
                f_score[ns] = tentative_g_score + h_score.get(ns[goal_index], math.inf)

                # Add neighbor to open list if not already present
                if ns not in [i[1] for i in open_list]:
                    heapq.heappush(open_list, (f_score[ns], ns))

    return []  # No path found