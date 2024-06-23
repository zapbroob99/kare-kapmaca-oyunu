# Squares Game

## Overview

This project implements a board game where players place pieces on a grid to form squares. The game can be played between two human players or against an AI opponent.

![image](https://github.com/zapbroob99/kare-kapmaca-oyunu/assets/87914525/22e428ee-2144-4d9d-a809-0e69f3f6a934)


## Requirements

- Python 3.x
- tkinter for GUI (optional)

## Files

- `main.py`: Contains the main logic for the game.
- `AIPlayer.py`: Contains the AI logic for playing the game.

## How to Play

### Human vs Human

1. Run `main.py`.
2. Players take turns to place their pieces on the board.
3. Players attempt to form squares with their pieces.
4. The game ends when a player is unable to place any more pieces or when a player forms more squares than the opponent.

### Human vs AI

1. Run `main.py`.
2. Follow the instructions to play against the AI.
3. The AI will take its turn after the human player.

## Game Rules

1. **Objective**: The objective of the game is to form as many squares as possible with your pieces on the board.
2. **Setup**: Players decide on the size of the grid (e.g., 6x6) before starting the game.
3. **Initial Placement**: 
    - Players take turns placing their pieces on the board one at a time.
    - Pieces can be placed on any empty space on the board.
    - The initial placement phase continues until all spaces are occupied or players decide to start the movement phase.
4. **Forming Squares**: 
    - A square is formed when four of a player's pieces occupy the four corners of a square on the grid.
    - Each square formed counts as one point.
5. **Movement Phase**:
    - After the initial placement phase, players can move their pieces.
    - Pieces can move to an adjacent empty space (up, down, left, right).
    - Players take turns moving one piece at a time.
6. **Taking Pieces**:
    - If a player forms a square, they can remove one of the opponent's pieces from the board.
    - The removed piece must not be part of a square.
7. **Winning the Game**:
    - The game ends when a player cannot make any more moves or when a player has formed more squares than their opponent.
    - The player with the most squares at the end of the game wins.

## Functions

### main.py

- `start_game()`: Prompts the player to enter the number of rows and columns for the game.
- `import_dict()`: Returns dictionaries for translating coordinates.
- `input_translation(input_o)`: Converts user input coordinates to board indices.
- `input_division(initial_input)`: Divides input into start and end coordinates.
- `check_space(pieces)`: Checks if there is an empty space on the board.
- `check_specific_space(pieces, selection)`: Checks if a specific space is occupied.
- `set_pieces(row, column)`: Initializes the board with empty spaces.
- `insert_piece(the_piece, pieces, color)`: Places a piece on the board.
- `remove_piece(the_piece, pieces)`: Removes a piece from the board.
- `count_squares(pieces, color)`: Counts the number of squares formed by a player's pieces.
- `is_square(pieces, the_piece)`: Checks if a piece is part of a square.
- `draw_board(a_pieces, highlight=None)`: Draws the game board.
- `initial_insertion_phase(pieces)`: Handles the initial phase of the game where players place their pieces.
- `get_valid_input_mono()`: Validates input format for placing pieces.
- `ai_initial_insertion_phase(pieces)`: Handles the initial phase of the game for AI vs Human.
- `is_there_any_piece_to_take(pieces, color)`: Checks if there are any pieces that can be taken.
- `piece_removal_by_ai(pieces, color="B", piece_amount=1)`: Handles piece removal by the AI.
- `piece_removal_by_player(pieces, color, piece_amount=1)`: Handles piece removal by the player.
- `piece_movement(pieces, the_piece, where_to, color)`: Moves a piece on the board.
- `pathway_check(pieces, the_piece, where_to)`: Checks if a piece can move to a desired coordinate.
- `can_move(pieces, the_piece)`: Checks if a piece can move.
- `ai_gameplay_phase(pieces, color="B")`: Handles the AI's turn during the gameplay phase.
- `gameplay_phase(pieces, color)`: Handles the player's turn during the gameplay phase.
- `get_valid_input()`: Validates input format for moving pieces.
- `how_many_pieces_left(pieces)`: Counts the remaining pieces for each player.
- `stuck_at_start(pieces)`: Checks if both players are stuck at the start of the game.
- `play()`: Main function for playing Human vs Human.
- `play_against_ai()`: Main function for playing Human vs AI.
- `main()`: Entry point of the program.

### AIPlayer.py

- `evaluate_board(pieces, ai_color, game_phase)`: Evaluates the board state for the AI.
- `ai_initial_placement(pieces, color)`: Determines the AI's initial placement of pieces.
- `ai_piece_removal(pieces, color)`: Determines which piece the AI will remove.
- `move_generate_possible_moves(pieces, color)`: Generates possible moves for the AI.
- `ai_gameplay_phase(pieces, color)`: Determines the AI's gameplay move.

## Running the Game

To start the game, run the `main.py` file. You will be prompted to enter the number of rows for the game board. Follow the on-screen instructions to play.

```sh
python main.py
