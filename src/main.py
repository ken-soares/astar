#!/usr/bin/env python3

import pygame
from board import Board

CELL_SIZE = 20
NB_CELLS = 16
WINDOW_SIZE = CELL_SIZE * NB_CELLS

WHITE = (255, 255, 255)
RED = (255, 0, 0)

def draw_board(window):
    board = Board(NB_CELLS)
    board.create_grid()

    for i in range(board.size):
        for j in range(board.size):
            if board.grid[i][j].is_goal:
                pygame.draw.rect(window, RED, (CELL_SIZE*i,
                                               CELL_SIZE*j,
                                               CELL_SIZE,
                                               CELL_SIZE))
            else:
                pygame.draw.rect(window, WHITE, (CELL_SIZE*i,
                                                 CELL_SIZE*j,
                                                 CELL_SIZE,
                                                 CELL_SIZE))
    pygame.display.flip()

def run():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def close_game():
    pygame.display.quit()
    pygame.quit()
    quit()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("A*")
    draw_board(window)
    run()
    close_game()
