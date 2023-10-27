from src.players.player import Player
from src import settings
import pygame
import sys


class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self.move_made = False

    def make_move(self, board):
        self.move_made = False
        while not self.move_made:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = int((y - settings.TOP_GRID_PADDING) // settings.BOARD_CELL_SIZE)
                    column = int((x - settings.LEFT_GRID_PADDING) // settings.BOARD_CELL_SIZE)

                    if board.add_move_to_board(row, column, self.color):
                        self.move_made = True
                        return True
                    else:
                        return False
