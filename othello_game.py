# Initialization of the board
import copy
import time


def init_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    return board


# Displaying the board
def display_board(board):
    print("  0 1 2 3 4 5 6 7")
    for i, row in enumerate(board):
        print(i, end=' ')
        for cell in row:
            print(cell.replace(" ", "_"), end=' ')
        print()


# Checking the validity of a move
def is_valid_move(board, x, y, player):
    opponent = 'W' if player == 'B' else 'B'
    if board[x][y] != ' ':
        return False, []

    directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
    flipped_cells = []

    for dx, dy in directions:
        temp_flips = []
        nx, ny = x + dx, y + dy
        while 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == opponent:
                temp_flips.append((nx, ny))
            elif board[nx][ny] == player:
                if temp_flips:
                    flipped_cells.extend(temp_flips)
                break
            else:
                break
            nx += dx
            ny += dy

    return len(flipped_cells) > 0, flipped_cells


# Applying a move on the board
def make_move(board, x, y, player):
    is_valid, flipped_cells = is_valid_move(board, x, y, player)
    if is_valid:
        board[x][y] = player
        for fx, fy in flipped_cells:
            board[fx][fy] = player
    return is_valid


# Transposition Table for storing already computed board evaluations
transposition_table = {}


# Improved evaluation function
def evaluate_board_advanced(board, player):
    player_score = 0
    opponent_score = 0
    opponent = 'W' if player == 'B' else 'B'

    # Board position values to prioritize corners and edges
    position_values = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4]
    ]

    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                player_score += position_values[i][j]
            elif board[i][j] == opponent:
                opponent_score += position_values[i][j]

    return player_score - opponent_score


# Alpha-Beta Pruned Min-Max algorithm with memory and time management
def alpha_beta_minmax(board, depth, alpha, beta, maximizing, active_player, timeout):
    if time.time() > timeout:
        return None, None

    board_str = ''.join(''.join(row) for row in board) + active_player
    if board_str in transposition_table:
        return transposition_table[board_str]

    if depth == 0:
        score = evaluate_board_advanced(board, active_player)
        transposition_table[board_str] = score, None
        return score, None

    best_move = None
    current_player = active_player if maximizing else ('W' if active_player == 'B' else 'B')

    if maximizing:
        max_eval = float('-inf')
        move_found = False  # Add this line
        for x in range(8):
            for y in range(8):
                new_board = copy.deepcopy(board)
                move_made = make_move(new_board, x, y, current_player)
                if move_made:
                    move_found = True  # Update this flag
                    eval_value, _ = alpha_beta_minmax(new_board, depth - 1, alpha, beta, False, active_player, timeout)
                    if eval_value is None:  # Timeout occurred
                        return None, None
                    if eval_value > max_eval:
                        max_eval = eval_value
                        best_move = (x, y)
                    alpha = max(alpha, eval_value)
                    if beta <= alpha:
                        break
        if not move_found:  # Check the flag here
            return evaluate_board_advanced(board, active_player), None
        transposition_table[board_str] = max_eval, best_move
        return max_eval, best_move

    else:
        min_eval = float('inf')
        move_found = False  # Add this line
        for x in range(8):
            for y in range(8):
                new_board = copy.deepcopy(board)
                move_made = make_move(new_board, x, y, current_player)
                if move_made:
                    move_found = True  # Update this flag
                    eval_value, _ = alpha_beta_minmax(new_board, depth - 1, alpha, beta, True, active_player, timeout)
                    if eval_value is None:  # Timeout occurred
                        return None, None
                    if eval_value < min_eval:
                        min_eval = eval_value
                        best_move = (x, y)
                    beta = min(beta, eval_value)
                    if beta <= alpha:
                        break
        if not move_found:  # Check the flag here
            return evaluate_board_advanced(board, active_player), None
        transposition_table[board_str] = min_eval, best_move
        return min_eval, best_move


# This will replace your existing `minmax_with_memory` function
def improved_minmax_with_memory(board, depth, maximizing, active_player, timeout):
    return alpha_beta_minmax(board, depth, float('-inf'), float('inf'), maximizing, active_player, timeout)


# Main function to play the game human vs AI
def play_game(player_turn_defined, depth_defined, max_timeout_defined):
    board = init_board()

    while True:
        display_board(board)

        if player_turn_defined == 'W':
            print("Human's turn:")
            x, y = get_human_move(board, 'W')
        else:
            print("AI's turn:")
            timeout = time.time() + max_timeout_defined  # 2-second timeout for AI
            _, (x, y) = improved_minmax_with_memory(board, depth_defined, True, 'B', timeout)
            if x is None and y is None:
                print("AI timeout. Human wins!")
                break

        make_move(board, x, y, player_turn_defined)

        # Checking for the end of the game
        if all(cell != ' ' for row in board for cell in row):
            w_score = sum(cell == 'W' for row in board for cell in row)
            b_score = sum(cell == 'B' for row in board for cell in row)
            print(f"Final scores - W: {w_score}, B: {b_score}")
            if w_score > b_score:
                print("Human wins!")
            elif b_score > w_score:
                print("AI wins!")
            else:
                print("It's a tie!")
            break

        player_turn_defined = 'B' if player_turn_defined == 'W' else 'W'


# Main function to play the game AI vs AI
def play_game_ai_vs_ai(player_turn_defined, depth_defined, max_timeout_defined):
    board = init_board()

    while True:
        print("Current board:")
        display_board(board)
        print(f"{player_turn_defined}'s turn:")

        for x in range(8):
            for y in range(8):
                valid, _ = is_valid_move(board, x, y, player_turn_defined)
                if valid:
                    print(f"Is move at ({x}, {y}) valid? {valid}")

        timeout = time.time() + max_timeout_defined  # 2-second timeout for AI
        score, (x, y) = improved_minmax_with_memory(board, depth_defined, True, player_turn_defined, timeout)
        print(f"Minmax returned score: {score}, move: ({x}, {y})")

        if x is None and y is None:
            print(f"{player_turn_defined} timeout. Game over!")
            break

        move_made = make_move(board, x, y, player_turn_defined)
        if move_made:
            print(f"AI placed at ({x}, {y}).")
        else:
            print("No valid move found.")

        # Checking for the end of the game
        w_valid_moves = any(is_valid_move(board, x, y, 'W')[0] for x in range(8) for y in range(8))
        b_valid_moves = any(is_valid_move(board, x, y, 'B')[0] for x in range(8) for y in range(8))

        if not (w_valid_moves or b_valid_moves):
            w_score = sum(cell == 'W' for row in board for cell in row)
            b_score = sum(cell == 'B' for row in board for cell in row)
            print(f"Final scores - W: {w_score}, B: {b_score}")
            if w_score > b_score:
                print("W wins!")
            elif b_score > w_score:
                print("B wins!")
            else:
                print("It's a tie!")
            break

        player_turn_defined = 'B' if player_turn_defined == 'W' else 'W'


# Function to get the human move
def get_human_move(board, player):
    while True:
        try:
            x, y = map(int,
                       input(f"Enter the coordinates where you want to place your '{player}' (row col): ").split())
            is_valid, _ = is_valid_move(board, x, y, player)
            if is_valid:
                return x, y
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")


# Main function to start the game
if __name__ == '__main__':
    player_turn = 'W'
    depth = 3  # You can adjust this as you like
    max_timeout = 600  # 60-second timeout for AI
    mode = input("Choose game mode (human or ai): ")
    if mode == 'human':
        play_game(player_turn, depth, max_timeout)
    elif mode == 'ai':
        play_game_ai_vs_ai(player_turn, depth, max_timeout)
    else:
        print("Invalid mode. Exiting.")
