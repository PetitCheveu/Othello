from time import sleep

import pygame
from src.board import Board
from src.players.ai_player import AIPlayer
from src.players.human_player import HumanPlayer
from src.menu import AIConfig, Menu


def main():
    clock = pygame.time.Clock()
    pygame.init()

    # Menu
    menu = Menu()
    chosen_game_mode = menu.run()

    # AI Config
    if chosen_game_mode == "Joueur vs. IA" or chosen_game_mode == "IA vs. IA":
        ai_config = AIConfig()
        ai_type, evaluating_method, depth, max_timeout = ai_config.run("First AI param")
        player2 = AIPlayer(color='W', ai_type=ai_type, evaluating_method=evaluating_method, depth=depth,
                           max_timeout=max_timeout)

        if chosen_game_mode == "IA vs. IA":
            ai_type, evaluating_method, depth, max_timeout = ai_config.run("Second AI param")
            player1 = AIPlayer(color='B', ai_type=ai_type, evaluating_method=evaluating_method, depth=depth,
                               max_timeout=max_timeout)

        else:
            player1 = HumanPlayer('B')

    else:
        player1 = HumanPlayer('B')
        player2 = HumanPlayer('W')

    board = Board()

    while True:
        move_made = False
        turn_skipped = False

        while not move_made:
            board.display_board()
            board.display_score()
            if player1.make_move(board):
                move_made = True
                turn_skipped = False
            else:
                board.display_invalid_move()
                sleep(0.3)

        if len(board.available_cells(player2.color)) == 0:
            if turn_skipped  or board.board_is_full():
                board.display_winner()
                sleep(5)
                break
            else:
                turn_skipped = True

        if player1 is AIPlayer:
            sleep(0.5)

        move_made = False
        while not move_made:
            board.display_board()
            board.display_score()
            if player2.make_move(board):
                move_made = True
                turn_skipped = False
            else:
                board.display_invalid_move()
                sleep(0.3)

        if len(board.available_cells(player1.color)) == 0:
            if turn_skipped or board.board_is_full():
                board.display_winner()
                sleep(5)
                break
            else:
                turn_skipped = True

        if player2 is AIPlayer:
            sleep(0.5)
        clock.tick(10)


if __name__ == "__main__":
    main()
