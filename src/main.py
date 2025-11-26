#!/usr/bin/env python3
from random import randint
import pygame as pg

import consts as c
import astar
from board import Board
    
def run(window : pg.Surface):
    # Initialize board
    board = Board(c.NB_CELLS)
    board.create_grid("src/board.txt")

    running = True

    # Tmp variables for astar testint
    search = False
    dest = [0, 0]  
    src = [0, 0]
    path = []

    while running:
        # Update game logic here

        # IMPORTANT !!!
        # The following part just tests the A* algorithm
        # The latter is ran once as we suppose nothing moves (collisions for instance) while the player is moving
        # Thus it is assumed that the source is static during the search
        if not search:
            dest[0] = randint(0, board.size - 1)
            dest[1] = randint(0, board.size - 1)

            src[0] = randint(0, board.size - 1)
            src[1] = randint(0, board.size - 1)

            board.clear_grid()
            board.clear_goal()
            board.set_goal(dest[0], dest[1])
            board.set_cell_value(src[0], src[1], 1)

            path = astar.astar(board, src, dest)

            search = True
        else:
            if not path:
                search = False
            else:
                pos = path.pop()
                board.set_cell_value(pos[0], pos[1], 1)


        # Rendering and Updating display
        board.draw(window)
        pg.display.flip()

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Sleep time
        pg.time.delay(200)
        

def close_game():
    pg.display.quit()
    pg.quit()
    quit()

def init():
    pg.init()
    
    window = pg.display.set_mode((c.WINDOW_SIZE, c.WINDOW_SIZE))
    pg.display.set_caption(c.WINDOW_TITLE)

    return window

def main():
    window = init()

    run(window)

    close_game()

if __name__ == "__main__":
    main()