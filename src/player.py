import pygame as pg

import consts as c

class Player():
    def __init__(self):
        self.timer = c.DECISION_TIME
        self.win_count = 0
        self.chosen_pawn = 1
        self.can_move = True
        self.move_count = 0
        self.move_sequence = []
    
    def play(self, event, board) -> tuple[int,int] :
        #initial_position = board.get_pawn_position(self.chosen_pawn)
        
        chosen_direction = -1

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                board.load_initial_state()
                self.move_count = 0
                self.move_sequence = []
                
            elif event.key == pg.K_UP and self.can_move:
                chosen_direction = c.MOVE_UP
                if board.move_pawn(chosen_direction, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_DOWN and self.can_move:
                chosen_direction = c.MOVE_DOWN
                if board.move_pawn(chosen_direction, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_LEFT and self.can_move:
                chosen_direction = c.MOVE_LEFT
                if board.move_pawn(chosen_direction, self.chosen_pawn):
                    self.move_count += 1
                    
            elif event.key == pg.K_RIGHT and self.can_move:
                chosen_direction = c.MOVE_RIGHT
                if board.move_pawn(chosen_direction, self.chosen_pawn):
                    self.move_count += 1

            elif event.key == pg.K_TAB:
                self.chosen_pawn = self.chosen_pawn % c.PAWN_NUMBER + 1

            elif event.key == pg.K_RETURN:
                self.chosen_pawn = -1
        
        return (self.chosen_pawn, chosen_direction)

    def check_solution_found(self, board) -> bool:
        (x, y) = board.get_pawn_position(self.chosen_pawn)
        if (board.grid[y][x].is_goal == 1) and (board.grid[y][x].goal_pawn_id == self.chosen_pawn):
            return True
        return False

    def reset(self):
        self.reset_timer()
        self.reset_move_sequence()
        self.chosen_pawn = 1
        self.move_count = 0
        self.can_move = True

    def increment_win_count(self):
        self.win_count += 1

    def get_win_count(self):
        return self.win_count

    def get_move_count(self):
        return self.move_count

    def get_chosen_pawn(self):
        return self.chosen_pawn
    
    def get_move_sequence(self):
        return self.move_sequence
    
    def reset_move_sequence(self):
        self.move_sequence = []

    def cannot_move(self):
        self.can_move = False
        
    def get_timer(self):
        return self.timer
    
    def decrement_timer(self):
        self.timer -= 1
    
    def reset_timer(self):
        self.timer = c.DECISION_TIME
