import copy
from random import random

import main


def evaluate_board(pieces, ai_color, game_phase):
    player_color = "W" if ai_color == "B" else "B"
    from main import count_squares
    ai_score = count_squares(pieces, ai_color)
    player_score = count_squares(pieces, player_color)
    if game_phase == 1:
        return ai_score - 2 * player_score
    elif game_phase == 3:
        return ai_score - player_score
    else:
        return ai_score - player_score


def phase1_generate_possible_moves(pieces):
    moves = []
    for row in range(len(pieces)):
        for col in range(len(pieces[row])):
            if pieces[row][col] == 0:
                moves.append((row, col))
    return moves


def phase2_generate_possible_moves(pieces, player_color):
    moves = []
    for row in range(len(pieces)):
        for col in range(len(pieces[row])):
            from main import is_square
            if pieces[row][col] == player_color and not is_square(pieces, (row, col)):
                moves.append((row, col))
    return moves


def phase3_generate_possible_moves(pieces, player_color):
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

def minimax(pieces, depth, is_maximizing, ai_color, game_phase):
    if depth == 0:
        return evaluate_board(pieces, ai_color, game_phase), None

    if game_phase == 1:
        possible_moves = phase1_generate_possible_moves(pieces)
    if game_phase==2:
        player_color = "W" if ai_color == "B" else "B"
        possible_moves = phase2_generate_possible_moves(pieces, player_color)
    if not possible_moves:
        return evaluate_board(pieces, ai_color, game_phase), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            row, col = move
            new_pieces = copy.deepcopy(pieces)
            if game_phase == 1:
                new_pieces[row][col] = ai_color
            else:
                new_pieces[row][col] = 0
            if (main.is_there_any_piece_to_take(pieces,ai_color)==True and game_phase==3): #Dynamically adapts and change the game phase if a piece removal can be done
                game_phase=2
            eval, _ = minimax(new_pieces, depth - 1, False, ai_color, game_phase)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        player_color = "W" if ai_color == "B" else "B"
        for move in possible_moves:
            row, col = move
            new_pieces = copy.deepcopy(pieces)
            if game_phase == 1:
                new_pieces[row][col] = player_color
            else:
                new_pieces[row][col] = 0
            eval, _ = minimax(new_pieces, depth - 1, True, ai_color, game_phase)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def minimax_phase3(pieces, depth, is_maximizing, ai_color):
    if depth == 0:
        return evaluate_board(pieces, ai_color,3), None

    possible_moves = phase3_generate_possible_moves(pieces, ai_color if is_maximizing else ("W" if ai_color == "B" else "B"))
    if not possible_moves:
        return evaluate_board(pieces, ai_color,3), None

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for move in possible_moves:
            board_copy = copy.deepcopy(pieces)
            (start_row, start_col), (end_row, end_col) = move
            board_copy[start_row][start_col], board_copy[end_row][end_col] = 0, ai_color
            eval, _ = minimax_phase3(board_copy, depth - 1, False, ai_color)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        player_color = "W" if ai_color == "B" else "B"
        for move in possible_moves:
            board_copy = copy.deepcopy(pieces)
            (start_row, start_col), (end_row, end_col) = move
            board_copy[start_row][start_col], board_copy[end_row][end_col] = 0, player_color
            eval, _ = minimax_phase3(board_copy, depth - 1, True, ai_color)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def ai_initial_placement(pieces, ai_color, depth=4):
    _, best_move = minimax(pieces, depth, True, ai_color, 1)
    return best_move




def ai_piece_removal(pieces, ai_color):
    _, best_move = minimax(pieces, 3, True, ai_color, 2)
    return best_move

def convert_move_to_string(start, end):
    start_row, start_col = start
    end_row, end_col = end
    start_str = f"{start_row + 1}{chr(start_col + ord('A'))}"
    end_str = f"{end_row + 1}{chr(end_col + ord('A'))}"
    return f"{start_str} {end_str}"


def ai_gameplay_phase(pieces, ai_color, depth=4):
    _, best_move = minimax_phase3(pieces, depth, True, ai_color)
    if best_move:
        return convert_move_to_string(*best_move)
    else:
        # Fallback: choose a random valid move if Minimax fails to find one
        possible_moves = phase3_generate_possible_moves(pieces, ai_color)
        if possible_moves:
            fallback_move = random.choice(possible_moves)
            return convert_move_to_string(*fallback_move)
        else:
            print("No valid moves")