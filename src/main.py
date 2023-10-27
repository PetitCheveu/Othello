import pygame
from src import menu, utils
from src.board import Board
from src.players.ai_player import AIPlayer
from src.players.human_player import HumanPlayer


def main():
    clock = pygame.time.Clock()
    pygame.init()

    chosen_game_mode = menu.menu()

    if chosen_game_mode == "Joueur vs. IA":
        ai_type1, evaluating_method1, depth1, max_timeout1 = menu.ai_parameters("AI param")

    if chosen_game_mode == "IA vs. IA":
        ai_type1, evaluating_method1, depth1, max_timeout1 = menu.ai_parameters("First AI param")
        ai_type2, evaluating_method2, depth2, max_timeout2 = menu.ai_parameters("Second AI param")

    board = Board()

    if chosen_game_mode == "Joueur vs. Joueur":
        player1 = HumanPlayer('B')
        player2 = HumanPlayer('W')

    elif chosen_game_mode == "Joueur vs. IA":
        player1 = HumanPlayer('B')
        player2 = AIPlayer(
            color='W',
            ai_type=ai_type1,
            evaluating_method=evaluating_method1,
            depth=depth1,
            max_timeout=max_timeout1
        )

    elif chosen_game_mode == "IA vs. IA":
        player1 = AIPlayer(
            color='B',
            ai_type=ai_type1,
            evaluating_method=evaluating_method1,
            depth=depth1,
            max_timeout=max_timeout1
        )
        player2 = AIPlayer(
            color='W',
            ai_type=ai_type2,
            evaluating_method=evaluating_method2,
            depth=depth2,
            max_timeout=max_timeout2
        )

    while True:
        board.display_board()
        board.display_score()
        board.board = player1.make_move(board.board)

        if not utils.has_valid_move(board.board, player2.color):
            break

        board.display_board()
        board.display_score()
        board.board = player2.make_move(board.board)

        if not utils.has_valid_move(board.board, player1.color):
            break

        clock.tick(10)


if __name__ == "__main__":
    main()
