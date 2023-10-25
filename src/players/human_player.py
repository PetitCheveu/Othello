from src.players.player import Player
from src import settings
import pygame
import sys
from src import utils


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
                    row = int((y - settings.TOP_GRID_PADDING) // settings.BOARD_CELL_SIZE)
                    column = int((x - settings.LEFT_GRID_PADDING) // settings.BOARD_CELL_SIZE)

                    is_valid, flipped_cells = utils.is_valid_move(board, row, column, self.color)

                    if is_valid:
                        board[row][column] = self.color
                        for fx, fy in flipped_cells:
                            board[fx][fy] = self.color
                        return board

        return None
