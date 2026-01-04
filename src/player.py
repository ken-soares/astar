import pygame as pg

from board import Board
import consts as c

class Player():
    def __init__(self):
        self.win_count : int = 0
        self.chosen_pawn : int = 1
        self.move_sequence = []

    def play(self, event : pg.event.Event, board : Board) -> None:      
        chosen_direction : int = -1

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                board.load_initial_state()
                self.reset()
            elif event.key == pg.K_UP:
                chosen_direction = c.MOVE_UP
                if board.move_pawn(self.chosen_pawn, chosen_direction):
                    self.move_sequence.append((self.chosen_pawn, chosen_direction))
            elif event.key == pg.K_DOWN:
                chosen_direction = c.MOVE_DOWN
                if board.move_pawn(self.chosen_pawn, chosen_direction):
                    self.move_sequence.append((self.chosen_pawn, chosen_direction))
            elif event.key == pg.K_LEFT:
                chosen_direction = c.MOVE_LEFT
                if board.move_pawn(self.chosen_pawn, chosen_direction):
                    self.move_sequence.append((self.chosen_pawn, chosen_direction))
            elif event.key == pg.K_RIGHT:
                chosen_direction = c.MOVE_RIGHT
                if board.move_pawn(self.chosen_pawn, chosen_direction):
                    self.move_sequence.append((self.chosen_pawn, chosen_direction))
            elif event.key == pg.K_TAB:
                self.chosen_pawn = self.chosen_pawn % c.PAWN_NUMBER + 1

    def reset(self) -> None:
        self.chosen_pawn = 1
        self.move_sequence = []

    def get_win_count(self) -> int:
        return self.win_count
    
    def increment_win_count(self) -> None:
        self.win_count += 1
    
    def get_move_sequence(self) -> list:
        return self.move_sequence

    def get_move_count(self) -> int:
        return len(self.move_sequence)  # O(1) operation

    def get_chosen_pawn(self) -> int:
        return self.chosen_pawn