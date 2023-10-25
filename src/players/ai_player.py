import copy
import time
from player import Player
import utils
MAX_SCORE = 1000000  # Choisissez une valeur appropriée pour MAX_SCORE

class AIPlayer(Player):

    def __init__(self, color, depth, max_timeout, ia_type, evaluating_method):
        super().__init__(color)  # AI always plays as 'B'
        self.depth = depth
        self.max_timeout = max_timeout
        self.ia_type = ia_type
        self.evaluating_method = evaluating_method
        self.memo = {}
        self.transposition_table = {}


    def make_move(self, board):
        if self.ia_type == "minmax" :
            possible_moves = utils.positions_jouables(board, self.color)
            return self.minmax_with_memory(board, self.depth, True, self.color, time.time() + self.max_timeout, possible_moves)
        elif self.ia_type == "alphabeta" :
            return self.improved_minmax_with_memory(board, self.depth, True, self.color, time.time() + self.max_timeout)

    # Fonction d'évaluation simple
    def evaluate_board(self, board, player):
        if self.evaluating_method == 1 : 
            return self.evaluate_board_by_position(board, player, 1)
        elif self.evaluating_method == 2 : 
            return self.evaluate_board_by_position(board, player, 2)
        elif self.evaluating_method == 3 :
            return self.evaluate_board_by_score(board, player)
        elif self.evaluating_method == 4 :
            return self.evaluate_board_by_mobility(board, player)
        
    def evaluate_board_by_score(self, board, player):
        player_score = sum(cell == player for row in board for cell in row)
        opponent_score = sum(cell != ' ' and cell != player for row in board for cell in row)
        return player_score - opponent_score
    
    def evaluate_board_by_mobility(self, board, player):
        opponent = 'W' if player == 'B' else 'B'

        # Poids pour chaque critère
        mobility_weight = 1.0  # Maximise la mobilité
        opponent_mobility_weight = -1.0  # Minimise la mobilité de l'adversaire
        corner_weight = 10.0  # Favorise la prise de coins

        # Compter la mobilité pour le joueur et l'adversaire
        player_mobility = len(utils.positions_jouables(board, player))
        opponent_mobility = len(utils.positions_jouables(board, opponent))

        # Compter les coins pris par le joueur et l'adversaire
        player_corners = sum([board[0][0], board[0][7], board[7][0], board[7][7]].count(player))
        opponent_corners = sum([board[0][0], board[0][7], board[7][0], board[7][7]].count(opponent))

        # Calculer le score en fonction des critères
        score = (
            mobility_weight * player_mobility +
            opponent_mobility_weight * opponent_mobility +
            corner_weight * (player_corners - opponent_corners)
        )

        return score
    
    def evaluate_board_by_position(self, board, player, evaluate_method):
        player_score = 0
        opponent_score = 0
        opponent = 'W' if player == 'B' else 'B'

        # Board position values to prioritize corners and edges
        if evaluate_method == 1:
            position_values = [
                [ 500, -150,  30,  10,  10,  30, -150,  500],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [ 30, 0,  1,  2,  2,  1, 0,  30],
                [ 10, 0,  2,  16,  16,  2, 0,  10],
                [ 10, 0,  2,  16,  16,  2, 0,  10],
                [ 30, 0,  1,  2,  2,  1, 0,  30],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [ 500, -150,  30,  10,  10,  30, -150,  500],
            ]
        elif evaluate_method == 2:
            position_values = [
                [ 100, -20,  10,  5,  5,  10, -20,  100],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [ 10, -2,  -1,  -1,  -1,  -1, -2,  10],
                [ 5, -2,  -1,  -1,  -1,  -1, -2,  5],
                [ 5, -2,  -1,  -1,  -1,  -1, -2,  5],
                [ 10, -2,  -1,  -1,  -1,  -1, -2,  10],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [ 100, -20,  10,  5,  5,  10, -20,  100],
            ]

        for i in range(8):
            for j in range(8):
                if board[i][j] == player:
                    player_score += position_values[i][j]
                elif board[i][j] == opponent:
                    opponent_score += position_values[i][j]

        return player_score - opponent_score
            
    def minmax_with_memory(self, board, depth, maximizing, player, timeout, possible_moves):
        if depth == 0:
            return self.evaluate_board(self, board, player), None

        if time.time() >= timeout:
            if not possible_moves:
                return self.evaluate_board(self, board, player), (-1, -1)

            best_move = possible_moves[0]
            return self.evaluate_board(self, board, player), best_move

        board_str = ''.join(''.join(row) for row in board) + player

        if board_str in self.memo:
            return self.memo[board_str]

        opponent = 'W' if player == 'B' else 'B'
        best_move = None

        if maximizing:
            max_eval = -MAX_SCORE
            for move in possible_moves:
                x, y = move
                new_board = copy.deepcopy(board)
                if utils.make_move(new_board, x, y, player):
                    eval_value, _ = self.minmax_with_memory(new_board, depth - 1, False, player, timeout, possible_moves)
                    if eval_value is None:
                        possible_moves.append((x, y))
                    elif eval_value > max_eval:
                        max_eval = eval_value
                        best_move = (x, y)
            if best_move is None:
                best_move = possible_moves[0]
                max_eval = self.evaluate_board(self, board, player)
            self.memo[board_str] = max_eval, best_move
            return max_eval, best_move
        else:
            min_eval = MAX_SCORE
            for move in possible_moves:
                x, y = move
                new_board = copy.deepcopy(board)
                if utils.make_move(new_board, x, y, opponent):
                    eval_value, _ = self.minmax_with_memory(new_board, depth - 1, True, player, timeout, possible_moves)
                    if eval_value is None:
                        possible_moves.append((x, y))
                    elif eval_value < min_eval:
                        min_eval = eval_value
                        best_move = (x, y)
            if best_move is None:
                best_move = possible_moves[0]
                min_eval = self.evaluate_board(self, board, player)
            self.memo[board_str] = min_eval, best_move
            return min_eval, best_move
        
    def alpha_beta_minmax(self, board, depth, alpha, beta, maximizing, active_player, timeout):
        if time.time() > timeout:
            return None, None

        board_str = ''.join(''.join(row) for row in board) + active_player
        if board_str in self.transposition_table:
            return self.transposition_table[board_str]

        if depth == 0:
            score = self.evaluate_board(self, board, active_player)
            self.transposition_table[board_str] = score, None
            return score, None

        best_move = None
        current_player = active_player if maximizing else ('W' if active_player == 'B' else 'B')

        if maximizing:
            max_eval = float('-inf')
            move_found = False  # Add this line
            for x in range(8):
                for y in range(8):
                    new_board = copy.deepcopy(board)
                    move_made = utils.make_move(new_board, x, y, current_player)
                    if move_made:
                        move_found = True  # Update this flag
                        eval_value, _ = self.alpha_beta_minmax(new_board, depth - 1, alpha, beta, False, active_player, timeout)
                        if eval_value is None:  # Timeout occurred
                            return None, None
                        if eval_value > max_eval:
                            max_eval = eval_value
                            best_move = (x, y)
                        alpha = max(alpha, eval_value)
                        if beta <= alpha:
                            break
            if not move_found:  # Check the flag here
                return self.evaluate_board(self, board, active_player), None
            self.transposition_table[board_str] = max_eval, best_move
            return max_eval, best_move

        else:
            min_eval = float('inf')
            move_found = False  # Add this line
            for x in range(8):
                for y in range(8):
                    new_board = copy.deepcopy(board)
                    move_made = utils.make_move(new_board, x, y, current_player)
                    if move_made:
                        move_found = True  # Update this flag
                        eval_value, _ = self.alpha_beta_minmax(new_board, depth - 1, alpha, beta, True, active_player, timeout)
                        if eval_value is None:  # Timeout occurred
                            return None, None
                        if eval_value < min_eval:
                            min_eval = eval_value
                            best_move = (x, y)
                        beta = min(beta, eval_value)
                        if beta <= alpha:
                            break
            if not move_found:  # Check the flag hereai
                return self.evaluate_board(self, board, active_player), None
            self.transposition_table[board_str] = min_eval, best_move
            return min_eval, best_move

    def improved_minmax_with_memory(self,board, depth, maximizing, active_player, timeout):
        return self.alpha_beta_minmax(board, depth, float('-inf'), float('inf'), maximizing, active_player, timeout)