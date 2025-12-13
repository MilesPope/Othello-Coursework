"""
Functions for the AI opponent, including thoes facilitating a level of performance
marginally worse than the player
"""

from game_engine import check_win, outflanked
from components import legal_move

def number_flipped(board:list, colour:str, coords:tuple[int,int]) -> int:
    """
    Check the amount of tokens that are flipped by a given move
    
    :param board: 2D array representing the board state
    :type board: list
    :param colour: the colour of the move that is made
    :type colour: str
    :param coords: the coordinates of the token placed
    :type coords: tuple[int, int]
    :return: the amount of tokens flipped by a move
    :rtype: int
    """

    # We can count the amount of flipped tokens by using the outflanked() function
    # First, see how many of the opponent's tokens there are before the token is placed
    # We already do this in check_win(), we can repurpose it here
    before_token_score = check_win(board)

    # Create a 'theoretical board' where the token is placed
    theoretical_board = [row.copy() for row in board]
    after_token_board = outflanked(theoretical_board, colour, coords)
    after_token_score = check_win(after_token_board)

    # check_win scores are given as (light, dark)
    score_index = 0 if colour == "Light" else 1

    # Calculate number of tokens flipped
    tokens_flipped = after_token_score[0][score_index] - before_token_score[0][score_index]

    return tokens_flipped

def possible_flip_counts(board:list, colour:str) -> dict:
    """
    The amount of tokens flipped by every legal move a given colour is able to make
    
    :param board: 2D list representing the board state
    :type board: list
    :param colour: string representing who's turn it is
    :type colour: str
    :return: dictionary containing coordinates, and number of tokens flipped
    :rtype: dict
    """
    return_dict = {}

    for x in range(len(board)):
        for y in range(len(board)):
            # For performance reasons, only check the moves that are legal
            if legal_move(colour, (x,y), board):
                tokens_flipepd = number_flipped(board, colour, (x,y))
                return_dict[(x,y)] = tokens_flipepd

    return return_dict

def choose_move(previous_flipped:int, possible_flips:dict) -> tuple | None:
    """
    Given a selection of possible (legal) moves, choose the one that meets these criteria:
        1. It is the number of tokens flipped closest to the user's previous moves
        2. If there is a draw, select the lower one so the AI is slightly worse than the user
    
    :param previous_flipped: integer representing the amount of tokens flipped by the previous move
    :type previous_flipped: int
    :param possible_flip_counts: a dictionary of coordinates and numbers of tokens that they flip
    :type possible_flip_counts: dict
    :return: the coordinates selected by the algorithm - the move that the 'AI' makes. 
    :rtype: tuple
    """

    if not possible_flips:
        return None

    # Beware monstrosity
    # Use absolute differences to find the closest to previous_flipped
    best_move = min ( # Take the minimum of...
        possible_flips.items(), # Each element represented as ((x,y), flip count)
        key=lambda item: ( # Apply a lambda function to each item to find:
            abs(item[1] - previous_flipped), # Distance from how many tokens the user's move flipped
            item[1] # And on a tie breaker, choose the one with the lover flip count
        )
    )[0]

    return best_move
