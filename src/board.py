import pygame

import settings


def init_board():
    board = [['_' for _ in range(settings.BOARD_SIZE)] for _ in range(settings.BOARD_SIZE)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    return board


def display_background_and_title(title=settings.CAPTION):
    window = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    window.fill(settings.GREEN)

    title = settings.TITLE_FONT.render(title, True, settings.BLACK)

    window.blit(
        title,
        title.get_rect(center=(settings.WINDOW_WIDTH // 2, 50))
    )

    return window


class Board:
    def __init__(self):
        self.board = init_board()
        self.window = display_background_and_title()

    def display_board(self):
        for row in range(settings.BOARD_SIZE):
            for column in range(settings.BOARD_SIZE):
                pygame.draw.rect(
                    self.window,
                    settings.LIGHT_BLUE,
                    pygame.Rect(
                        settings.LEFT_GRID_PADDING + column * settings.BOARD_CELL_SIZE,
                        settings.TOP_GRID_PADDING + row * settings.BOARD_CELL_SIZE,
                        settings.BOARD_CELL_SIZE,
                        settings.BOARD_CELL_SIZE
                    ),
                    1
                )
                pygame.draw.circle(
                    self.window,
                    settings.BLACK if self.board[row][column] == 'B' else settings.WHITE if self.board[row][column] == 'W' else settings.GREEN,
                    (
                        settings.LEFT_GRID_PADDING + column * settings.BOARD_CELL_SIZE + settings.BOARD_CELL_SIZE // 2,
                        settings.TOP_GRID_PADDING + row * settings.BOARD_CELL_SIZE + settings.BOARD_CELL_SIZE // 2
                    ),
                    settings.BOARD_CELL_SIZE // 2 - 5
                )

        pygame.display.flip()

    def display_score(self):
        black_score = sum(row.count('B') for row in self.board)
        white_score = sum(row.count('W') for row in self.board)
        total_score = black_score + white_score
        player_turn = 'noir' if total_score % 2 == 0 else 'blanc'

        texts = [
            (f"Noir: {black_score}", 20),
            (f"Blanc: {white_score}", 60),
            (f"Tour: {total_score}", 100),
            (f"Joueur: {player_turn}", 140)
        ]

        for text, y_position in texts:
            rendered_text = settings.FONT.render(text, True, settings.BLACK)
            self.window.blit(rendered_text, rendered_text.get_rect(topright=(settings.WINDOW_WIDTH - 20, y_position)))

        button_texts = ["Quitter", "Rejouer"]
        for i, button_text in enumerate(button_texts):
            pygame.draw.rect(self.window, settings.LIGHT_BLUE,
                             (settings.WINDOW_WIDTH - 100, settings.WINDOW_HEIGHT - 60 - i * 60, 80, 40))
            rendered_button_text = settings.FONT.render(button_text, True, settings.BLACK)
            self.window.blit(rendered_button_text, rendered_button_text.get_rect(
                center=(settings.WINDOW_WIDTH - 60, settings.WINDOW_HEIGHT - 40 - i * 60)))

        pygame.display.flip()

    def display_winner(self):
        self.display_board()

        black_score = sum(row.count('B') for row in self.board)
        white_score = sum(row.count('W') for row in self.board)

        winner = 'noir' if black_score > white_score else 'blanc' if white_score > black_score else 'aucun'
        winner_text = settings.FONT.render(
            "Match nul !" if winner == 'aucun' else f"Le gagnant est le joueur {winner} !",
            True,
            settings.BLACK
        )
        winner_rect = pygame.Rect(
            0,
            settings.WINDOW_HEIGHT - 100,
            settings.WINDOW_WIDTH,
            50
        )

        pygame.draw.rect(
            self.window,
            settings.GREEN,
            winner_rect
        )

        self.window.blit(
            winner_text,
            winner_text.get_rect(center=winner_rect.center)
        )

        pygame.display.flip()
