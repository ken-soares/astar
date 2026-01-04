#!/usr/bin/env python3
from collections import deque
import math, copy, threading, concurrent.futures

import pygame as pg

import consts as c
import astar

from board import Board
from player import Player
    
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
    font = pg.font.SysFont('Consolas', 18)

    # Game state variables
    running : bool = True
    game_state : int = c.STATE_INITIALIZING
    timer : int = -1
    solution_found : bool = False
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    ai_future = None
    ai_cancel = threading.Event()
    ai_board : Board = None
    ai_score : int = 0
    ai_moves : int = 0
    ai_move_sequence : list = []
    ai_move_timer : int = 0
    heuristic : dict = {} 
    gui_args : list = [-1, False, 0, 0] # 0: remaining time, 1: solution found flag, 2: AI score, 3: AI moves

    # Game loop
    while running:
        # Update game logic here
        match game_state:
            case c.STATE_INITIALIZING:
                player.reset()

                board.clear()
                board.choose_goal()

                # Calc heuristic here
                goal_pos = board.get_goal()
                heuristic  = {(x, y): math.inf for x in range(c.NB_CELLS) for y in range(c.NB_CELLS)} # Dummy initial value
                heuristic[goal_pos] = 0

                queue : deque = deque()
                queue.append(goal_pos)

                while queue:
                    x, y = queue.popleft()

                    for direction in [c.MOVE_UP, c.MOVE_DOWN, c.MOVE_LEFT, c.MOVE_RIGHT]:

                        n_x, n_y = board.simulate_move((x, y), direction)

                        if (n_x, n_y) != (-1, -1):
                            if heuristic[(n_x, n_y)] > heuristic[(x, y)] + 1:
                                heuristic[(n_x, n_y)] = heuristic[(x, y)] + 1
                                queue.append((n_x, n_y))

                board.init_pawns()
                board.save_initial_state()

                timer = c.DECISION_TIME
                solution_found = False
                ai_move_sequence = []
                ai_moves = 0
                ai_move_timer = 0

                game_state = c.STATE_PLAYER_TURN
            case c.STATE_PLAYER_TURN:
                for event in pg.event.get():
                    player.play(event, board)

                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == TIMER_EVENT:
                        if timer > 0:
                            timer -= 1

                            goal_pos : tuple[int,int] = board.get_goal()
                            goal_id : int = board.get_goal_color()
                            target_pawn_pos : tuple[int,int] = board.get_pawn(goal_id)

                            if target_pawn_pos == goal_pos:
                                solution_found = True
                                game_state = c.STATE_PLAYER_END
                        else:
                            game_state = c.STATE_PLAYER_END
            case c.STATE_PLAYER_END:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            if not solution_found:
                                player.get_move_sequence().clear()

                            board.load_initial_state()

                            ai_cancel.clear()
                            ai_board = copy.deepcopy(board)
                            ai_future = executor.submit(astar.astar, ai_board, heuristic, ai_cancel)

                            timer = c.DECISION_TIME
                            solution_found = False

                            game_state = c.STATE_COMPUTER_CALCULATING
            case c.STATE_COMPUTER_CALCULATING:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == TIMER_EVENT:
                        if timer > 0:
                            timer -= 1

                            if ai_future is not None and ai_future.done():
                                ai_move_sequence = ai_future.result()  # result is safe to use in main thread
                                ai_moves = len(ai_move_sequence) - 1
                                ai_future = None
                                game_state = c.STATE_COMPUTER_TURN
                        else:
                            ai_cancel.set()
                            ai_future.cancel()

                            game_state = c.STATE_RESULTS # No solution found within time
                            if player.get_move_count() > 0:
                                player.increment_win_count()
            case c.STATE_COMPUTER_TURN:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False

                current_time = pg.time.get_ticks()

                if len(ai_move_sequence) > 0:
                    if current_time - ai_move_timer >= 2000: # 2 seconds per move
                        ai_move_timer = current_time
                        board.clear_pawns()

                        state : tuple = ai_move_sequence.pop()

                        for i in range(c.PAWN_NUMBER):
                            x, y = state[i]
                            board.set_cell_value(x, y, i + 1)
                else:
                    # If AI found a better path, or player did not find any solution then AI scores
                    if player.get_move_count() == 0 or ai_moves < player.get_move_count():
                        ai_score += 1
                    else:
                        if ai_moves == player.get_move_count():
                            ai_score += 1
                        player.increment_win_count()

                    game_state = c.STATE_RESULTS
            case c.STATE_RESULTS:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            game_state = c.STATE_INITIALIZING
            case _:
                print("Unhandled game state! Halting...")
                running = False

        # Update GUI arguments
        gui_args[0] = timer
        gui_args[1] = solution_found
        gui_args[2] = ai_score
        gui_args[3] = ai_moves

         # Rendering and Updating display
        window.fill(c.BLACK) # Clear the window with black color

        board.draw(window)

        render_gui(window, font, game_state, player, gui_args)

        pg.display.flip()

        # Sleep to maintain 60 FPS
        clock.tick(60)

def render_gui(window: pg.Surface, font: pg.font.Font, game_state: int, player: Player, args: list) -> None:
    # Unpack arguments
    remaining_time : int = args[0]
    solution_found : bool = args[1]
    ai_score : int = args[2]
    ai_moves: int = args[3]

    # Render GUI based on game state
    match game_state:
        case c.STATE_INITIALIZING:
            info_text = font.render("Initializing...", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))
        case c.STATE_PLAYER_TURN:
            move_count : int = player.get_move_count()
            chosen_pawn : int = player.get_chosen_pawn()
            win_count : int = player.get_win_count()

            info_text = font.render("Player's turn!", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))

            timer_text = font.render(f"Time left: {remaining_time} s", False, c.WHITE)
            window.blit(timer_text, (400, c.WINDOW_SIZE + 10))

            move_text = font.render(f"Moves made: {move_count}", False, c.WHITE)
            window.blit(move_text, (10, c.WINDOW_SIZE + 40))

            pawn_text = font.render("Chosen pawn: " + c.COLOR_NAME_MAP[c.PAWN_COLORS[chosen_pawn]], False, c.WHITE)
            window.blit(pawn_text, (200, c.WINDOW_SIZE + 40))

            wins_text = font.render(f"Score: {win_count}", False, c.WHITE)
            window.blit(wins_text, (400, c.WINDOW_SIZE + 40))

            cmd_text = font.render("Arrows: Move   Tab: Change pawn   Esc: Return to initial state", False, c.WHITE)
            window.blit(cmd_text, (10, c.WINDOW_SIZE + 100))
        case c.STATE_PLAYER_END:
            move_count : int = player.get_move_count()

            info_text = font.render("Time is up!", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))

            text : str = f"You did not find a solution in time. Total moves: {move_count}."
            if solution_found:
                text = f"You found a solution in {move_count} moves."

            move_text = font.render(text, False, c.WHITE)
            window.blit(move_text, (10, c.WINDOW_SIZE + 40))

            prompt_text = font.render("Press ENTER to continue.", False, c.WHITE)
            window.blit(prompt_text, (10, c.WINDOW_SIZE + 70))
        case c.STATE_COMPUTER_CALCULATING:
            info_text = font.render("Computing best path...", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))

            timer_text = font.render(f"Time left: {remaining_time} s", False, c.WHITE)
            window.blit(timer_text, (400, c.WINDOW_SIZE + 10))
        case c.STATE_COMPUTER_TURN:
            info_text = font.render("Computer's turn!", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))

            score_text = font.render(f"AI Score: {ai_score}", False, c.WHITE)
            window.blit(score_text, (400, c.WINDOW_SIZE + 10))

            move_text = font.render(f"Moves made: {ai_moves}", False, c.WHITE)
            window.blit(move_text, (10, c.WINDOW_SIZE + 40))
        case c.STATE_RESULTS:
            info_text = font.render("Results:", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))

            win_count : int = player.get_win_count()

            wins_text = font.render(f"Score: {win_count}", False, c.WHITE)
            window.blit(wins_text, (200, c.WINDOW_SIZE + 40))

            score_text = font.render(f"AI Score: {ai_score}", False, c.WHITE)
            window.blit(score_text, (200, c.WINDOW_SIZE + 70))

            prompt_text = font.render("Press ENTER to continue.", False, c.WHITE)
            window.blit(prompt_text, (10, c.WINDOW_SIZE + 100))
        case _:
            info_text = font.render("Unknown game state!", False, c.WHITE)
            window.blit(info_text, (10, c.WINDOW_SIZE + 10))
        
def close_game():
    pg.display.quit()
    pg.quit()
    quit()

def init():
    pg.init()
    
    window = pg.display.set_mode((c.WINDOW_SIZE, c.WINDOW_SIZE + c.WINDOW_GUI_HEIGHT))
    pg.display.set_caption(c.WINDOW_TITLE)
    pg.time.set_timer(pg.USEREVENT, 1000) # creates an event that counts seconds

    return window

def main():
    window = init()

    run(window)

    close_game()

if __name__ == "__main__":
    main()