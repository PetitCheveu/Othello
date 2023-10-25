import pygame
import menu
from board import Board


def main():
    clock = pygame.time.Clock()
    pygame.init()

    chosen_game_mode = menu.menu()

    if chosen_game_mode == "PVIA":
        ai, deepness = menu.ai_parameters("AI param")

    if chosen_game_mode == "IAVIA":
        ai1, deepness1 = menu.ai_parameters("First AI param")
        ai2, deepness2 = menu.ai_parameters("Second AI param")

    board = Board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        board.display_board()
        board.display_score()
        clock.tick(10)


if __name__ == "__main__":
    main()
