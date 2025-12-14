#!/usr/bin/env python3
from random import randint
import pygame as pg

import consts as c
import astar
from board import Board
from player import Player

def are_coordinates_unique(coords_list):
    seen = set()
    for coord in coords_list:
        if coord in seen:
            return False
        seen.add(coord)
    return True

def generate_unique_coordinates(board, num_coordinates):
    coordinates = []
    attempts = 0
    max_attempts = board.size * board.size
    
    while len(coordinates) < num_coordinates and attempts < max_attempts:
        x = randint(0, board.size - 1)
        y = randint(0, board.size - 1)
        coord = (x, y)
        
        if coord not in coordinates:
            coordinates.append(coord)
        
        attempts += 1
    
    if len(coordinates) < num_coordinates:
        print(f"Warning: Could not generate {num_coordinates} unique coordinates on a {board.size}x{board.size} board")
    
    return coordinates

    
def run(window : pg.Surface):

    TIMER_EVENT = pg.USEREVENT
    clock = pg.time.Clock()
    
    # Initialize board
    board = Board(c.NB_CELLS)
    board.create_grid("src/board.txt")
    
    player = Player()
    font = pg.font.SysFont('Consolas', 20)

    running = True

    # Tmp variables for astar testint
    search = False
    dest = [0, 0]
    src1 = [0, 0]
    src2 = [0, 0]
    src3 = [0, 0]

    all_coords = generate_unique_coordinates(board, 4)

    if len(all_coords) >= 4:
        dest[0], dest[1] = all_coords[0]
        src1[0], src1[1] = all_coords[1]
        src2[0], src2[1] = all_coords[2]
        src3[0], src3[1] = all_coords[3]
        
        goal_pawn_id = randint(1, 3)
        
        board.set_cell_value(src1[0], src1[1], 1)
        board.set_cell_value(src2[0], src2[1], 2)
        board.set_cell_value(src3[0], src3[1], 3)
        
        board.set_goal(dest[0], dest[1], goal_pawn_id)

    # save board state so we can rollback on our turn if we find another path
    board.save_initial_state()

    while running:
        # Update game logic here

        # IMPORTANT !!!
        # The following part just tests the A* algorithm
        # The latter is ran once as we suppose nothing moves (collisions for instance) while the player is moving
        # Thus it is assumed that the source is static during the search
        #if not search:
        #    dest[0] = randint(0, board.size - 1)
        #    dest[1] = randint(0, board.size - 1)

        #    src[0] = randint(0, board.size - 1)
        #    src[1] = randint(0, board.size - 1)

        #    board.clear_grid()
        #    board.clear_goal()

        #    path = astar.astar(board, src, dest)

        #    search = True
        #else:
            #if not path:
            #    search = False
            #else:
            #    pos = path.pop()
            #    board.set_cell_value(pos[0], pos[1], 1)


        # Rendering and Updating display

        # Handle events
        for event in pg.event.get():
            player.play(event, board)
            if event.type == pg.QUIT:
                running = False
            elif event.type == TIMER_EVENT:
                if player.get_timer() > 0:
                    player.decrement_timer()
                else:
                    pg.time.set_timer(TIMER_EVENT, 0)

        # fps limit at 60
        time_text = font.render("time left: " + str(player.get_timer()).rjust(3), True, (255, 255, 255))
        move_count_text = font.render("move count: " + str(player.get_move_count()), True, (255,255,255))
        chosen_pawn_text = font.render("moving pawn: " + board.get_pawn_colors()[player.get_chosen_pawn() - 1], True, (255,255,255))
        window.fill((0, 0, 0))
        window.blit(time_text, (10, c.WINDOW_SIZE + 10))
        window.blit(move_count_text, (10, c.WINDOW_SIZE + 35))
        window.blit(chosen_pawn_text, (10, c.WINDOW_SIZE + 55))
        
        board.draw(window)
        pg.display.flip()
        clock.tick(60)
        

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