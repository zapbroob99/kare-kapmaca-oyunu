import threading
import time

import AIPlayer
import game_gui
import tkinter


def start_game():
    # Takes row number from the player, checks and returns it.
    row_number = input("Please enter the number of horizontal lines [3,7]:")
    check = row_number.isdigit()
    while check == False:
        row_number = input("Please enter the number of horizontal lines [3,7]:")
        check = row_number.isdigit()
    row_number = int(row_number)
    while row_number < 3 or row_number > 7:
        print("Please enter a number between 3 and 7")
        row_number = input("Please enter the number of horizontal lines [3,7]:")
        check = row_number.isdigit()
        while check == False:
            row_number = input("Please enter the number of horizontal lines [3,7]:")
            check = row_number.isdigit()
        row_number = int(row_number)
    column_number = row_number + 1
    return row_number, column_number


def import_dict():
    # Matches the coordinates entered by the user with the indexes of the lists with the help of a dictionary.
    # Returns the resulting dictionaries.
    dict_y = {
        "A": "0",
        "B": "1",
        "C": "2",
        "D": "3",
        "E": "4",
        "F": "5",
        "G": "6",
        "H": "7"
    }
    dict_x = {
        "1": "0",
        "2": "1",
        "3": "2",
        "4": "3",
        "5": "4",
        "6": "5",
        "7": "6"
    }
    return dict_x, dict_y


def input_translation(input_o):
    # Converts the variables to avoid int-string mismatch.
    dict_x, dict_y = import_dict()
    x = dict_x[input_o[0]]
    y = dict_y[input_o[1]]
    output = f"{x}{y}"
    return output


def input_division(initial_input):
    output_one = f"{initial_input[0]}{initial_input[1]}"
    output_two = f"{initial_input[3]}{initial_input[4]}"
    output_one_translated = input_translation(output_one)
    output_two_translated = input_translation(output_two)
    return output_one_translated, output_two_translated


def check_space(pieces):
    # Examines the board for an empty point. Returns a boolean.
    is_board_empty = False
    a = 0
    while a < len(pieces):
        if 0 in pieces[a]:
            is_board_empty = True
        a += 1
    return is_board_empty


def check_specific_space(pieces, selection):
    # Takes the list of pieces and the selected point as parameters. Returns which piece a selected point belongs to
    # or is empty.
    try:
        x = int(selection[0])
        y = int(selection[1])
        return pieces[x][y]
    except:
        pass


def set_pieces(row, column):
    # Takes row and column numbers as parameters. Creates and returns the empty list where the pieces will be stored.
    initial_pieces = [0] * row
    for i in range(row):
        initial_pieces[i] = [0] * column
    return initial_pieces


def insert_piece(the_piece, pieces, color):
    # Takes the coordinate of the point (the_piece), the list of pieces (pieces) and the color it belongs to as
    # parameters. Places the piece at the desired coordinate.
    x = int(the_piece[0])
    y = int(the_piece[1])
    if pieces[x][y] == 0:
        pieces[x][y] = color


def remove_piece(the_piece, pieces):
    # removes a piece from the board.
    # the_piece: piece to be removed , pieces: list of all pieces.
    x = int(the_piece[0])
    y = int(the_piece[1])
    if pieces[x][y] != 0:
        pieces[x][y] = 0
    return pieces[x][y]


def count_squares(pieces, color):
    # Takes the positions and the player as parameter, returns an integer (number of squares) back.
    square_count = 0
    for i in range(len(pieces)):
        for k in range(len(pieces[i])):
            try:
                if pieces[i][k] == pieces[i][k + 1] == pieces[i + 1][k] == pieces[i + 1][k + 1] == color:
                    square_count += 1
            except:
                pass
    return square_count


def is_square(pieces, the_piece):
    # Checks if a piece belongs to a square or not.
    check = False
    try:
        x = int(the_piece[0])
        y = int(the_piece[1])


    except:
        pass

    try:
        if pieces[x][y] == pieces[x][y + 1] == pieces[x + 1][y] == pieces[x + 1][y + 1]:
            check = True

    except:
        pass
    try:
        if pieces[x - 1][y] == pieces[x - 1][y + 1] == pieces[x][y] == pieces[x][y + 1]:
            check = True
    except:
        pass
    try:
        if pieces[x][y - 1] == pieces[x][y] == pieces[x + 1][y - 1] == pieces[x + 1][y]:
            check = True
    except:
        pass
    try:
        if pieces[x - 1][y - 1] == pieces[x - 1][y] == pieces[x][y - 1] == pieces[x][y]:
            check = True
    except:
        pass

    return check


def draw_board(a_pieces, highlight=None):
    # ANSI escape code for red color
    RED = '\033[91m'
    # ANSI escape code to reset color
    RESET = '\033[0m'
    # Convert highlight to a tuple of integers if it's not None
    if highlight is not None:
        highlight = (int(highlight[0]), int(highlight[1]))
    # Prints the pieces with the coordinates in accordance with the list.
    pieces = list(a_pieces)
    row_number = len(pieces)
    column_number = row_number + 1
    dict = {
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
        8: "H"
    }
    space = " "
    twospace = "  "
    bigspace = "   "
    for i in range(1, row_number + 2):
        if i != 1:
            for element in range(1, column_number + 1):
                if element == column_number:
                    if highlight and (i - 2, element - 1) == highlight:
                        print(RED + f"{pieces[i - 2][element - 1]}" + RESET, end="", sep='')
                    else:
                        print(pieces[i - 2][element - 1], end="", sep='')
                elif element != 1:
                    if highlight and (i - 2, element - 1) == highlight:
                        print(RED + f"[{pieces[i - 2][element - 1]}]" + RESET, "---", end="", sep='')
                    else:
                        print(pieces[i - 2][element - 1], "---", end="", sep='')
                else:
                    if highlight and (i - 2, element - 1) == highlight:
                        print(space + RED + f"[{pieces[i - 2][element - 1]}]" + RESET + "---", end="", sep='')
                    else:
                        print(space, pieces[i - 2][element - 1], "---", end="", sep='')
        if i == 1:
            for element in range(1, column_number + 1):
                if element != 1:
                    print(bigspace, dict[element], end="", sep='')
                else:
                    print(twospace, dict[element], end="", sep='')

        if i != row_number + 1:
            print("")
            if i != 1:
                line = "|   "
                print(twospace + line * (row_number + 1))
            print(i, end="")
        if i == row_number + 1:
            pass
    print("")
    print("------------------------------------------")


def initial_insertion_phase(pieces):
    # First phase of game.
    # Players insert their pieces until there's no space left.
    player_turn = 1
    while check_space(pieces) == True:
        if player_turn == 1:
            draw_board(pieces)
            selection = input("Select an empty space for your piece (Player One):")
            selection = input_translation(selection.upper())
            while check_specific_space(pieces, selection) != 0:
                selection = input("Select an empty space for your piece (Player One):")
                selection = input_translation(selection.upper())
            insert_piece(selection, pieces, "W")
            player_turn += 1
        else:
            draw_board(pieces)
            selection = input("Select an empty space for your piece (Player Two):")
            selection = input_translation(selection.upper())
            while check_specific_space(pieces, selection) != 0:
                selection = input("Select an empty space for your piece (Player Two):")
                selection = input_translation(selection.upper())
            insert_piece(selection, pieces, "B")
            player_turn -= 1


def ai_initial_insertion_phase(pieces):
    # First phase of game.
    # Players insert their pieces until there's no space left.
    player_turn = 1
    while check_space(pieces):
        if player_turn == 1:
            selection = input("Select an empty space for your piece (Player One):")
            selection = input_translation(selection.upper())
            while check_specific_space(pieces, selection) != 0:
                selection = input("Select an empty space for your piece (Player One):")
                selection = input_translation(selection.upper())
            insert_piece(selection, pieces, "W")
            player_turn += 1

        else:
            # AI's turn

            # Assuming you have a function ai_select_move() that returns the AI's move
            ai_move = AIPlayer.ai_initial_placement(pieces, "B")

            while check_specific_space(pieces, ai_move) != 0:
                ai_move = AIPlayer.ai_initial_placement(pieces)
                ai_move = input_translation(ai_move.upper())

            insert_piece(ai_move, pieces, "B")
            print("Computer has insterted piece:")
            player_turn -= 1
        draw_board(pieces)


def is_there_any_piece_to_take(pieces, color):
    can_take = False
    non_square_piece = 0
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            if pieces[i][j] == color:
                piece = f"{i}{j}"
                if is_square(pieces, piece) == False:
                    non_square_piece += 1
    if non_square_piece > 0:
        can_take = True
    return can_take


def piece_removal_by_ai(pieces, color="B", piece_amount=1):
    # Second phase of game.
    # Players remove opponent's pieces in proportion to the number of squares they have.
    how_many_removes = piece_amount
    if color == "W":
        player = "one"
        opponent = "B"
    else:
        player = "two"
        opponent = "W"
    can_take = is_there_any_piece_to_take(pieces, opponent)
    if not can_take:
        print(f"Player {player} cant take any piece!")
    else:
        if how_many_removes > 0:
            while 0 < how_many_removes:
                if how_many_removes == 1:
                    is_it_plural = "piece"
                else:
                    is_it_plural = "pieces"
                draw_board(pieces)
                print(f"Player {player} can remove {how_many_removes} {is_it_plural}!")
                is_it_square = False
                is_it_opponents = False
                selection = AIPlayer.ai_piece_removal(pieces, color)
                remove_piece(selection, pieces)
                how_many_removes -= 1
            else:
                print(f"Player {player} used all of his/her removals!")
        else:
            print(f"Player {player} has no square!")


def piece_removal_by_player(pieces, color, piece_amount=1):
    # Second phase of game.
    # Players remove opponent's pieces in proportion to the number of squares they have.
    how_many_removes = piece_amount
    if color == "W":
        player = "one"
        opponent = "B"
    else:
        player = "two"
        opponent = "W"
    can_take = is_there_any_piece_to_take(pieces, opponent)
    if can_take == False:
        print(f"Player {player} cant take any piece!")
    else:
        if how_many_removes > 0:
            while 0 < how_many_removes:
                if how_many_removes == 1:
                    is_it_plural = "piece"
                else:
                    is_it_plural = "pieces"
                draw_board(pieces)
                print(f"Player {player} can remove {how_many_removes} {is_it_plural}!")
                is_it_square = False
                is_it_opponents = False
                while is_it_opponents == False or is_it_square == False:
                    selection = input(
                        f"Please select a piece which isnt a part of a square to remove from opponent (Player {player}):")
                    selection = input_translation(selection.upper())
                    if check_specific_space(pieces, selection) == color or check_specific_space(pieces, selection) == 0:
                        is_it_opponents = False
                        print("Selected space doesn't have any piece of opponent's.")
                    else:
                        is_it_opponents = True
                    if is_square(pieces, selection):
                        is_it_square = False
                        print("Selected space has a piece which is a part of a square.")
                    else:
                        is_it_square = True
                remove_piece(selection, pieces)
                how_many_removes -= 1
            else:
                print(f"Player {player} used all of his/her removals!")
        else:
            print(f"Player {player} has no square!")


def piece_movement(pieces, the_piece, where_to, color):
    # Moves a piece using functions remove_piece() and insert_piece().
    remove_piece(the_piece, pieces)
    insert_piece(where_to, pieces, color)
    return where_to


def pathway_check(pieces, the_piece, where_to):
    # Checks if a piece can go to a desired coordinate.
    can_go = True
    x = int(the_piece[0])
    y = int(the_piece[1])
    xx = int(where_to[0])
    yy = int(where_to[1])
    if the_piece == where_to:
        can_go = False
    else:
        if x != xx and y != yy:
            can_go = False
        else:
            if y > yy:
                for i in range(yy, y):
                    if check_specific_space(pieces, f"{x}{i}") != 0:
                        can_go = False
            else:
                if y < yy:
                    for i in range(y + 1, yy + 1):
                        if check_specific_space(pieces, f"{x}{i}") != 0:
                            can_go = False
            if x > xx:
                for i in range(xx, x):
                    if check_specific_space(pieces, f"{i}{y}") != 0:
                        can_go = False
            else:
                if x < xx:
                    for i in range(x + 1, xx + 1):
                        if check_specific_space(pieces, f"{i}{y}") != 0:
                            can_go = False

    return can_go


def can_move(pieces, the_piece):
    can_move = True
    count = 0
    x = int(the_piece[0])
    y = int(the_piece[1])
    up = f"{x - 1}{y}"
    down = f"{x + 1}{y}"
    left = f"{x}{y - 1}"
    right = f"{x}{y + 1}"
    if x == 0:
        up = f"{x}{y}"
    elif x == len(pieces) - 1:
        down = f"{x}{y}"
    if y == 0:
        left = f"{x}{y}"
    elif y == len(pieces[0]) - 1:
        right = f"{x}{y}"
    if pathway_check(pieces, the_piece, up) == False:
        count += 1
    if pathway_check(pieces, the_piece, down) == False:
        count += 1
    if pathway_check(pieces, the_piece, left) == False:
        count += 1
    if pathway_check(pieces, the_piece, right) == False:
        count += 1
    if count == 4:
        can_move = False
    return can_move


def ai_gameplay_phase(pieces, color="B"):
    player = "two"
    possible_moves = AIPlayer.move_generate_possible_moves(pieces, color)
    if not possible_moves:
        print(f"Player {player} has no valid moves. Passing the turn.")
        return  # Pass the turn
    available = False
    movable = False
    while available == False or movable == False:
        initial_input = AIPlayer.ai_gameplay_phase(pieces, color)
        selection, where_to = input_division(initial_input)
        if check_specific_space(pieces, selection) != color or can_move(pieces, selection) is False:
            print("Please select your own available pieces!")
        else:
            available = True
        if pathway_check(pieces, selection, where_to) is False:
            print("Please select a movable space!")
        else:
            movable = True
    piece_movement(pieces, selection, where_to, color)
    draw_board(pieces, highlight=where_to)  # Highlight the moved piece
    print(" AI Moved piece")
    if is_square(pieces, where_to) == True:
        piece_removal_by_ai(pieces)
    else:
        piece_amount = 0
        piece_removal_by_ai(pieces, color, piece_amount)


def gameplay_phase(pieces, color):
    draw_board(pieces)
    if color == "W":
        player = "one"
    else:
        player = "two"
    available = False
    movable = False
    possible_moves = AIPlayer.move_generate_possible_moves(pieces, color)
    if not possible_moves:
        print(f"Player {player} has no valid moves. Passing the turn.")
        return  # Pass the turn
    while available == False or movable == False:
        initial_input = input(f"Please select a piece and a position to move (Player {player}):")
        initial_input = initial_input.upper()
        selection, where_to = input_division(initial_input)
        if check_specific_space(pieces, selection) != color or can_move(pieces, selection) == False:
            print("Please select your own available pieces!")
        else:
            available = True
        if pathway_check(pieces, selection, where_to) == False:
            print("Please select a movable space!")
        else:
            movable = True
    piece_movement(pieces, selection, where_to, color)
    if is_square(pieces, where_to) == True:
        piece_removal_by_player(pieces, color)
    else:
        piece_amount = 0
        piece_removal_by_player(pieces, color, piece_amount)


def how_many_pieces_left(pieces):
    whites_amount = 0
    blacks_amount = 0
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            piece = f"{i}{j}"
            if check_specific_space(pieces, piece) == "W":
                whites_amount += 1
            elif check_specific_space(pieces, piece) == "B":
                blacks_amount += 1
            else:
                pass
    return whites_amount, blacks_amount


def stuck_at_start(pieces):
    not_stuck = 0
    for i in range(len(pieces)):
        for j in range(len(pieces[i])):
            piece = f"{i}{j}"
            if can_move(pieces, piece) == True:
                not_stuck += 1
    if not_stuck == 0:
        return True
    else:
        return False


def play():
    player_turn = 1
    pieces = set_pieces(*start_game())
    initial_insertion_phase(pieces)
    piece_removal_by_player(pieces, "W", count_squares(pieces, "W"))
    piece_removal_by_player(pieces, "B", count_squares(pieces, "B"))
    if stuck_at_start(pieces) == True:
        print("Both player got stuck at the beggining. Player one will take first piece.")
        is_it_opponents = False
        while is_it_opponents == False:
            draw_board(pieces)
            selection = input(f"Please select a piece remove from opponent (Player one):")
            selection = input_translation(selection.upper())
            if check_specific_space(pieces, selection) == "W" or check_specific_space(pieces, selection) == 0:
                is_it_opponents = False
                print("Selected space doesn't have any piece of opponent's.")
            else:
                is_it_opponents = True
        remove_piece(selection, pieces)
        player_turn += 1
    black_pieces = 4
    white_pieces = 4
    while black_pieces > 3 and white_pieces > 3:
        if player_turn == 1:
            color = "W"
            player_turn += 1
        else:
            color = "B"
            player_turn -= 1
        gameplay_phase(pieces, color)
        white_pieces, black_pieces = how_many_pieces_left(pieces)

    if white_pieces > 3:
        print("Player one has won with whites!!")
    else:
        print("Player two has won with blacks!!")


def play_against_ai():

    player_turn = 1
    pieces = set_pieces(4, 5)
    draw_board(pieces)
    ai_initial_insertion_phase(pieces)
    piece_removal_by_player(pieces, "W", count_squares(pieces, "W"))
    piece_removal_by_ai(pieces, "B", count_squares(pieces, "B"))
    if stuck_at_start(pieces) == True:
        print("Both player got stuck at the beggining. Player one will take first piece.")
        is_it_opponents = False
        while is_it_opponents == False:
            draw_board(pieces)
            selection = input(f"Please select a piece remove from opponent (Player one):")
            selection = input_translation(selection.upper())
            if check_specific_space(pieces, selection) == "W" or check_specific_space(pieces, selection) == 0:
                is_it_opponents = False
                print("Selected space doesn't have any piece of opponent's.")
            else:
                is_it_opponents = True
        remove_piece(selection, pieces)
        player_turn += 1
    black_pieces = 4
    white_pieces = 4
    while black_pieces > 3 and white_pieces > 3:
        if player_turn == 1:
            color = "W"
            player_turn += 1
            gameplay_phase(pieces, color)
        else:
            color = "B"
            player_turn -= 1
            ai_gameplay_phase(pieces, color)
        white_pieces, black_pieces = how_many_pieces_left(pieces)
    draw_board(pieces)
    if white_pieces > 3:
        print("Player one has won with whites!!")
    else:
        print("Player two has won with blacks!!")


def main():
    play_against_ai()


if __name__ == "__main__":
    main()
