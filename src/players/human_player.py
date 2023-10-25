from player import Player
import settings
import pygame
import sys
import utils

class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color)

    def make_move(self, board):
        move_made = False
        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = (y - settings.TOP_GRID_PADDING) // settings.BOARD_CELL_SIZE
                    column = (x - settings.LEFT_GRID_PADDING) // settings.BOARD_CELL_SIZE
                    is_valid, _ = utils.is_valid_move(board, row, column, self.color)
                    if is_valid:
                        move_made = True
                        return row, column

        return None, None  # En cas de problème ou de sortie prématurée