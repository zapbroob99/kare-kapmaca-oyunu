import copy
import random

import main


def evaluate_board(pieces, ai_color, game_phase):
    player_color = "W" if ai_color == "B" else "B"

    # Count the number of squares controlled by each player
    from main import count_squares
    ai_square_count = count_squares(pieces, ai_color)  # Number of squares controlled by AI
    player_square_count = count_squares(pieces, player_color)  # Number of squares controlled by opponent

    # Calculate center control
    center_control = 0
    center_points = [(2, 2), (2, 3), (3, 2), (3, 3)]  # Center points for a 5x6 board
    for row, col in center_points:
        if pieces[row][col] == ai_color:
            center_control += 1
        elif pieces[row][col] == player_color:
            center_control -= 1

    # Penalize positions where vulnerable pieces are far from squares controlled by AI
    vulnerable_penalty = 0
    for row in range(len(pieces)):
        for col in range(len(pieces[0])):
            if pieces[row][col] == ai_color:  # AI's piece
                # Check if the piece is vulnerable (not part of a square)
                from main import is_square
                if not is_square(pieces, (row, col)):
                    # Calculate the distance to the nearest AI-controlled square
                    min_distance = float('inf')
                    for i, j in center_points:
                        if pieces[i][j] == ai_color:
                            distance = abs(row - i) + abs(col - j)
                            min_distance = min(min_distance, distance)
                    vulnerable_penalty -= min_distance

    # Evaluate based on game phase
    if game_phase == 1:
        # During initial placement, prioritize center control and minimizing vulnerable pieces' distance to squares
        return 20* ai_square_count - 30 * player_square_count + center_control + vulnerable_penalty
    elif game_phase == 3:
        # During regular gameplay, focus on overall square control and minimizing vulnerable pieces' distance to squares
        return ai_square_count - player_square_count + center_control + vulnerable_penalty
    else:
        # For other game phases, use a similar evaluation as regular gameplay
        return ai_square_count - player_square_count + center_control + vulnerable_penalty



def insertion_generate_possible_moves(pieces):
    moves = []
    for row in range(len(pieces)):
        for col in range(len(pieces[row])):
            if pieces[row][col] == 0:
                moves.append((row, col))
    return moves


def removal_generate_possible_moves(pieces, player_color):
    moves = []
    for row in range(len(pieces)):
        for col in range(len(pieces[row])):
            from main import is_square
            if pieces[row][col] == player_color and not is_square(pieces, (row, col)):
                moves.append((row, col))
    return moves


def move_generate_possible_moves(pieces, player_color):
    moves = []
    for row in range(len(pieces)):
        for col in range(len(pieces[row])):
            if pieces[row][col] == player_color:
                for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + drow, col + dcol
                    if 0 <= new_row < len(pieces) and 0 <= new_col < len(pieces[row]):
                        from main import pathway_check
                        if pieces[new_row][new_col] == 0 and pathway_check(pieces, (row, col), (new_row, new_col)):
                            moves.append(((row, col), (new_row, new_col)))
    return moves


def minimax(pieces, depth, is_maximizing, ai_color, game_phase, alpha, beta):
    if depth == 0:
        return evaluate_board(pieces, ai_color, game_phase), None

    if game_phase == 1:
        possible_moves = insertion_generate_possible_moves(pieces)
    elif game_phase == 2:
        player_color = "W" if ai_color == "B" else "B"
        possible_moves = removal_generate_possible_moves(pieces, player_color)
    else:
        possible_moves = move_generate_possible_moves(pieces,
                                                      ai_color if is_maximizing else ("W" if ai_color == "B" else "B"))

    if not possible_moves:
        return evaluate_board(pieces, ai_color, game_phase), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            new_pieces = copy.deepcopy(pieces)
            if game_phase == 1:
                row, col = move
                new_pieces[row][col] = ai_color
            elif game_phase == 2:
                row, col = move
                new_pieces[row][col] = 0
            else:
                start, end = move
                start_row, start_col = start
                end_row, end_col = end
                new_pieces[start_row][start_col], new_pieces[end_row][end_col] = 0, ai_color

            if game_phase == 3 and main.is_there_any_piece_to_take(new_pieces, ai_color):
                eval, _ = minimax(new_pieces, depth - 1, False, ai_color, 2, alpha, beta)
            else:
                eval, _ = minimax(new_pieces, depth - 1, False, ai_color, game_phase, alpha, beta)

            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        player_color = "W" if ai_color == "B" else "B"
        for move in possible_moves:
            new_pieces = copy.deepcopy(pieces)
            if game_phase == 1:
                row, col = move
                new_pieces[row][col] = player_color
            elif game_phase == 2:
                row, col = move
                new_pieces[row][col] = 0
            else:
                start, end = move
                start_row, start_col = start
                end_row, end_col = end
                new_pieces[start_row][start_col], new_pieces[end_row][end_col] = 0, player_color

            if game_phase == 3 and main.is_there_any_piece_to_take(new_pieces, player_color):
                eval, _ = minimax(new_pieces, depth - 1, True, ai_color, 2, alpha, beta)
            else:
                eval, _ = minimax(new_pieces, depth - 1, True, ai_color, game_phase, alpha, beta)

            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def ai_initial_placement(pieces, ai_color, depth=4):
    _, best_move = minimax(pieces, depth, True, ai_color, 1, float('-inf'), float('inf'))
    return best_move


def ai_piece_removal(pieces, ai_color):
    _, best_move = minimax(pieces, 5, True, ai_color, 2, float('-inf'), float('inf'))
    return best_move


def convert_move_to_string(start, end):
    start_row, start_col = start
    end_row, end_col = end
    start_str = f"{start_row + 1}{chr(start_col + ord('A'))}"
    end_str = f"{end_row + 1}{chr(end_col + ord('A'))}"
    return f"{start_str} {end_str}"


def ai_gameplay_phase(pieces, ai_color, depth=5):
    _, best_move = minimax(pieces, depth, True, ai_color, 3, float('-inf'), float('inf'))
    if best_move:
        return convert_move_to_string(*best_move)
    else:
        # Fallback: choose a random valid move if Minimax fails to find one
        possible_moves = move_generate_possible_moves(pieces, ai_color)
        if possible_moves:
            fallback_move = random.choice(possible_moves)
            return convert_move_to_string(*fallback_move)
        else:
            print("No valid moves")
