#!/usr/bin/env python3
from random import randint
import pygame as pg

import consts as c
import astar
from board import Board
from player import Player

## TODO: Move these functions to another file like utils.py
def are_coordinates_unique(coords_list):
    seen = set()
    for coord in coords_list:
        if coord in seen:
            return False
        seen.add(coord)
    return True

def generate_unique_coordinates(board):
    coordinates = []
    illegal_coords = []
    illegal_coords.append((7,7))
    illegal_coords.append((7,8))
    illegal_coords.append((8,7))
    illegal_coords.append((8,8))

    for key, tuples in c.PAWN_GOAL_COORDS.items():
        for c1, c2 in tuples:
            illegal_coords.append((c1, c2))

    while len(coordinates) < c.PAWN_NUMBER:
        x = randint(0, board.size - 1)
        y = randint(0, board.size - 1)
        coord = (x, y)

        if coord not in illegal_coords:
            #if coord not in [(key, c1, c2) for key, tuples in c.PAWN_GOAL_COORDS.items() for c1, c2 in tuples]:
                coordinates.append(coord)
    
    return coordinates
## END OF REGION

def prepare_board(board : Board):
    src1 = [0, 0]
    src2 = [0, 0]
    src3 = [0, 0]
    src4 = [0, 0]

    all_coords = generate_unique_coordinates(board)

    if len(all_coords) >= 4:
        src1[0], src1[1] = all_coords[0]
        src2[0], src2[1] = all_coords[1]
        src3[0], src3[1] = all_coords[2]
        src4[0], src4[1] = all_coords[3]
        
        goal_pawn_id = randint(1, 4)
        goal_coords_id = randint(0,3)

        dest_line, dest_col = c.PAWN_GOAL_COORDS[goal_pawn_id][goal_coords_id]

        board.set_cell_value(src1[0], src1[1], 1)
        board.set_cell_value(src2[0], src2[1], 2)
        board.set_cell_value(src3[0], src3[1], 3)
        board.set_cell_value(src4[0], src4[1], 4)
        
        board.set_goal(dest_line, dest_col, goal_pawn_id)

        return 0
    return -1

def clear_board(board : Board):
    board.clear_pawns()
    board.clear_goal()
    
def run(window : pg.Surface):
    # Initialize clock and timer event
    TIMER_EVENT = pg.USEREVENT
    clock = pg.time.Clock()
    
    # Initialize board
    board = Board(c.NB_CELLS)
    board.create_grid("src/board.txt")
    
    # Initialize player
    player = Player()

    # Initialize font
    font = pg.font.SysFont('Consolas', 20)

    running = True

    prepare_board(board)

    # save board state so we can rollback on our turn if we find another path
    board.save_initial_state()

    solution_found = False
    put_on_pause = False
    current_turn_win = False
    ai_move_sequence = []
    move_sequence = []

    while running:
        # Update game logic here
        for event in pg.event.get():
            pawn, direction = player.play(event, board)

            if direction != -1:
                player.get_move_sequence().append((pawn, direction))
            elif pawn == -1:
                restart_game(player, board, TIMER_EVENT)
                solution_found = False
                put_on_pause = False
                current_turn_win = False
                ai_move_sequence = []
                move_sequence = []

            if event.type == pg.QUIT:
                running = False
            elif event.type == TIMER_EVENT:

                if player.get_timer() > 0:
                    if(player.check_solution_found(board)):
                        solution_found = True
                        put_on_pause = True
                    player.decrement_timer()
                else:
                    #print("Timer expired!")
                    put_on_pause = True

                if put_on_pause:
                    move_sequence = player.get_move_sequence()
                    pause_game(player, TIMER_EVENT)
                    board.load_initial_state()
                    ai_move_sequence = astar.astar(board, board.get_pawn_position(1), board.get_goal())
                    if solution_found:
                        if compare_with_ai(ai_move_sequence, move_sequence):
                            current_turn_win = True
                            player.increment_win_count()
                
        
         # Rendering and Updating display
        window.fill(c.BLACK) # Clear the window with black color

        board.draw(window)

        # TODO: THIS MUST BE MOVED INTO ANTOTHER FUNCTION
        remaining_time = player.get_timer()
        move_count = player.get_move_count()
        chosen_pawn = player.get_chosen_pawn()

        time_text = font.render("Time left: " + str(remaining_time).rjust(3), True, c.WHITE)
        win_text = font.render("                                        Wins: " + str(player.get_win_count()), True, c.WHITE)
        move_count_text = font.render("Move count: " + str(move_count), True, c.WHITE)
        chosen_pawn_text = font.render("Moving pawn: " + c.COLOR_NAME_MAP[c.PAWN_COLORS[chosen_pawn]], True, c.WHITE)
        
        window.blit(time_text, (10, c.WINDOW_SIZE + 10))
        window.blit(win_text, (10, c.WINDOW_SIZE + 10))
        window.blit(move_count_text, (10, c.WINDOW_SIZE + 35))
        window.blit(chosen_pawn_text, (10, c.WINDOW_SIZE + 55))

        if put_on_pause:
            if solution_found:
                solution_found_text = font.render("Move sequence for solution: " + str(move_sequence), True, c.WHITE)
                window.blit(solution_found_text, (10, c.WINDOW_SIZE + 80))
            else:
                timeout_text = font.render("Timer expired ! ", True, c.WHITE)
                window.blit(timeout_text, (10, c.WINDOW_SIZE + 100))
            if not current_turn_win:
                solution_found_text = font.render("Computer's solution: " + str(ai_move_sequence), True, c.WHITE)
                window.blit(solution_found_text, (10, c.WINDOW_SIZE + 120))
            
        
        # END OF REGION

        #print( player.get_move_sequence())

        pg.display.flip()

        # Sleep to maintain 60 FPS
        clock.tick(60)

def compare_with_ai(ai_move_sequence, move_sequence) -> bool:
    if len(move_sequence) >= len(ai_move_sequence):
        return True
    return False

def pause_game(player: Player, timer_event):
    pg.time.set_timer(timer_event, 0)
    player.cannot_move()

def restart_game(player : Player, board : Board, timer_event):
    player.reset()
    clear_board(board)
    prepare_board(board)
    board.save_initial_state()
    pg.time.set_timer(timer_event, 1000)
        
def close_game():
    pg.display.quit()
    pg.quit()
    quit()

def init():
    pg.init()
    
    window = pg.display.set_mode((c.WINDOW_SIZE, c.WINDOW_SIZE + 150))
    pg.display.set_caption(c.WINDOW_TITLE)
    pg.time.set_timer(pg.USEREVENT, 1000) # creates an event that counts seconds

    return window

def main():
    window = init()

    run(window)

    close_game()

if __name__ == "__main__":
    main()