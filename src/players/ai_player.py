import copy
import time

from src.board import Board
from src.players.player import Player
from src import settings

MAX_SCORE = 1000000


class AIPlayer(Player):

    def __init__(self, color, ai_type, evaluating_method, max_timeout=settings.MAX_TIMEOUT, depth=6):
        super().__init__(color)  # AI always plays as 'B'
        self.depth = depth
        self.max_timeout = max_timeout
        self.ai_type = ai_type
        self.evaluating_method = evaluating_method
        self.memo = {}
        self.transposition_table = {}

    def make_move(self, board):
        move_to_make = None

        if self.ai_type == settings.AVAILABLE_AIS.keys()[0]:
            available_cells = board.available_cells(self.color)

            move_to_make = self.minmax_with_memory(
                board=board,
                maximizing=True,
                timeout=time.time() + self.max_timeout,
                available_moves=available_cells,
                depth=self.depth
            )[1]

        elif self.ai_type == settings.AVAILABLE_AIS.keys()[1]:

            move_to_make = self.alpha_beta_minmax(
                board=board,
                alpha=float('-inf'),
                beta=float('inf'),
                maximizing=True,
                timeout=time.time() + self.max_timeout,
                depth=self.depth
            )[1]

        board.add_move_to_board(move_to_make[0], move_to_make[1], self.color)

    def minmax_with_memory(self, board, maximizing, timeout, available_moves, depth):

        opponent = 'W' if self.color == 'B' else 'B'
        best_move = None
        board_str = ''.join(''.join(row) for row in board.board) + self.color

        if self.depth == 0:
            return board.evaluate_board(self), None

        if time.time() >= timeout:

            if not available_moves:
                return board.evaluate_board(self), (-1, -1)

            best_move = available_moves[0]

            return board.evaluate_board(self), best_move

        if board_str in self.memo:
            return self.memo[board_str]

        if maximizing:
            max_eval = -MAX_SCORE

            for move in available_moves:
                x, y = move
                new_board = Board()
                new_board.board = copy.deepcopy(board.board)

                if new_board.add_move_to_board(x, y, self.color):
                    eval_value, _ = self.minmax_with_memory(new_board, False, timeout,
                                                            available_moves, depth=depth - 1)

                    if eval_value is None:
                        available_moves.append((x, y))

                    elif eval_value > max_eval:
                        max_eval = eval_value
                        best_move = (x, y)

            if best_move is None:
                best_move = available_moves[0]
                max_eval = board.evaluate_board(self)

            self.memo[board_str] = max_eval, best_move

            return max_eval, best_move

        else:
            min_eval = MAX_SCORE

            for move in available_moves:
                x, y = move
                new_board = Board()
                new_board.board = copy.deepcopy(board.board)

                if new_board.add_move_to_board(x, y, opponent):
                    eval_value, _ = self.minmax_with_memory(new_board, True, timeout,
                                                            available_moves, depth=depth - 1)

                    if eval_value is None:
                        available_moves.append((x, y))

                    elif eval_value < min_eval:
                        min_eval = eval_value
                        best_move = (x, y)

            if best_move is None:
                best_move = available_moves[0]
                min_eval = board.evaluate_board(self)

            self.memo[board_str] = min_eval, best_move

            print("minimal evaluation: ", min_eval)
            return min_eval, best_move

    def alpha_beta_minmax(self, board, alpha, beta, maximizing, timeout, depth):
        board_str = ''.join(''.join(row) for row in board) + self.color
        best_move = None
        current_player = self.color if maximizing else ('W' if self.color == 'B' else 'B')

        if time.time() > timeout:
            return None, None

        if board_str in self.transposition_table:
            return self.transposition_table[board_str]

        if depth == 0:
            score = board.evaluate_board(self)
            self.transposition_table[board_str] = score, None
            return score, None

        if maximizing:
            max_eval = float('-inf')
            move_found = False

            for x in range(8):

                for y in range(8):
                    new_board = Board()
                    new_board.board = copy.deepcopy(board.board)
                    move_made = new_board.add_move_to_board(x, y, current_player)

                    if move_made:
                        move_found = True  # Update this flag
                        eval_value, _ = self.alpha_beta_minmax(
                            board=new_board,
                            alpha=alpha,
                            beta=beta,
                            maximizing=False,
                            timeout=timeout,
                            depth=depth - 1
                        )

                        if eval_value is None:  # Timeout occurred
                            return None, None

                        if eval_value > max_eval:
                            max_eval = eval_value
                            best_move = (x, y)

                        alpha = max(alpha, eval_value)

                        if beta <= alpha:
                            break

            if not move_found:  # Check the flag here
                return board.evaluate_board(self), None

            self.transposition_table[board_str] = max_eval, best_move

            return max_eval, best_move

        else:
            min_eval = float('inf')
            move_found = False

            for x in range(8):

                for y in range(8):

                    new_board = Board()
                    new_board.board = copy.deepcopy(board.board)
                    move_made = new_board.add_move_to_board(x, y, current_player)

                    if move_made:
                        move_found = True

                        eval_value, _ = self.alpha_beta_minmax(
                            board=new_board,
                            alpha=alpha,
                            beta=beta,
                            maximizing=True,
                            timeout=timeout,
                            depth=depth - 1
                        )

                        if eval_value is None:  # Timeout occurred
                            return None, None

                        if eval_value < min_eval:
                            min_eval = eval_value
                            best_move = (x, y)

                        beta = min(beta, eval_value)

                        if beta <= alpha:
                            break

            if not move_found:  # Check the flag here
                return board.evaluate_board(self), None

            self.transposition_table[board_str] = min_eval, best_move

            return min_eval, best_move
