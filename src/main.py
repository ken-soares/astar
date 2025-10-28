#!/usr/bin/env python3

import pygame

WINDOW_SIZE = 500

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
    run()
    close_game()
