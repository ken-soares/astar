import pygame as pg

import consts as c

class Player():
    def __init__(self):
        self.timer = c.DECISION_TIME
        self.chosen_pawn = 1
        self.move_count = 0
    
    def reset_timer(self):
        self.timer = c.DECISION_TIME
    
    #todo store all moves to reset
    def play(self, event, board):
        initial_position = board.get_pawn_position(self.chosen_pawn)
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                board.reset_to_initial()
                self.move_count = 0
                
            elif event.key == pg.K_UP:
                if board.move_pawn(c.MOVE_UP, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_DOWN:
                if board.move_pawn(c.MOVE_DOWN, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_LEFT:
                if board.move_pawn(c.MOVE_LEFT, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_RIGHT:
                if board.move_pawn(c.MOVE_RIGHT, self.chosen_pawn):
                    self.move_count += 1

            elif event.key == pg.K_TAB:
                self.chosen_pawn = self.chosen_pawn % 3 + 1

    def get_move_count(self):
        return self.move_count

    def get_chosen_pawn(self):
        return self.chosen_pawn

    def decrement_timer(self):
        self.timer -= 1
        
    def get_timer(self):
        return self.timer
