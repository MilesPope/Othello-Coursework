"""
Module providing initialisation functions for board and methods to print and check legal moves
"""

from colorama import Fore

def initialise_board(size:int = 8) -> list:
    """
    Return an initialised Othello board for the given size
    
    :param size: Board dimension (default 8)
    :type size: int
    :return: 2D list representing starting board
    :rtype: list
    """

    # Board size must be even from starting 2x2 tokens
    if size % 2 != 0:
        raise ValueError("Board size must be an even number")
    # Board size must be positive and greater than two
    if size < 2:
        raise ValueError("Board size must be greater than two")
    # Initialise the board:
    board = []

    # Fill in board
    for _ in range(size):
        board.append([None] * size)

    # Place starting tokens
    mid = size // 2

    board[mid-1][mid-1] = "Light"
    board[mid-1][mid] = "Dark "
    board[mid][mid-1] = "Dark "
    board[mid][mid] = "Light"

    # Return the initialised board
    return board

def print_board(board:list) -> None:
    """
    Print an ASCII representation of the board state to the command line
    
    :param board: variable dimension list
    :type board: list
    """

    representation_map = {
        "Light" : "W",
        "Dark " : "B",
        None : "N"
    }
    colour_map = {
        "Light" : Fore.GREEN,
        "Dark " : Fore.RED,
        None: Fore.WHITE
    }

    for row in board:
        for cell in row:
            try:
                cell_representation = representation_map[cell]
                colour_representation = colour_map[cell]
            except KeyError:
                raise KeyError(f"Unrecognised board entry {cell}") from None
            print(colour_representation + "|" + cell_representation + "|", end="")
        print("\n")

def legal_move(colour:str, coord:tuple, board:list) -> bool:
    """
    Check whether a given move of placing a counter at a coordinate as a player is a legal move
    
    :param colour: either "Dark " or "Light" depending on who's turn it is
    :type colour: str
    :param coord: coordinate to check
    :type coord: tuple
    :param board: given board
    :type board: list
    :return: boolean statement saying whether move is legal or not.
    :rtype: bool
    """

    # Initialise variables
    x = coord[0]
    y = coord[1]
    opponent = "Dark " if colour == "Light" else "Light"
    board_size = len(board)

    # Check whether coordinate is empty
    try:
        if board[y][x] is not None:
            return False
    except IndexError:
        raise IndexError from None

    # Check whether coordinate outflanks at least once peice
    # Go through each direction to check there is at least one line containing at,
    # least one opposing peice followed by one player peice
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:

            # Skip (0,0)
            if dx == 0 and dy == 0:
                continue

            neighbour_x = x + dx
            neighbour_y = y + dy


            # Skip if out of bounrs
            if not (0 <= neighbour_x < board_size and 0 <= neighbour_y < board_size):
                continue

            # Skip if next token is not opponent's peice
            if board[neighbour_y][neighbour_x] != opponent:
                continue

            # At this stage we know the next token in the line is an opponent peice
            # Go through, and check if its a string of opponent peices
            # AND terminated by player's peice
            next_x = neighbour_x
            next_y = neighbour_y

            # Continue going until we meet a break case
            while True:
                next_x += dx
                next_y += dy

                # Break if out of bounds:
                if not (0 <= next_x < board_size and 0 <= next_y < board_size):
                    break

                # Break if no token
                if board[next_y][next_x] is None:
                    break

                # If the next peice belongs to player then we have a legal move!
                if board[next_y][next_x] == colour:
                    # print(f"Found legal for ({x},{y}) with line ({dx},{dy})")
                    return True # yay!
    # If we go through all possible lines without a hit, no legal moves!
    return False
