"""
Module containing main game loop
"""

from components import initialise_board, legal_move, print_board

def cli_coords_input() -> tuple:
    """
    Get an input for coordinates from the client
    
    :return: inputted coordinates if they are valid
    :rtype: tuple
    """
    valid_input = False
    while not valid_input:
        try:
            x_coord = int(input("Enter x coordinate: "))
            y_coord = int(input("Enter y coordinate: "))
            if x_coord < 0 or y_coord < 0:
                print("Coordinates must be positive")
            else:
                valid_input = True
        except TypeError:
            print("Enter an integer")
        except ValueError:
            print("Do not enter a blank string")
    # print("abc")
    return (x_coord,y_coord)

def outflanked(board:list, colour:str, coords:list) -> list:
    """
    Change outflanked tokens to the player's colour
    
    :param board: current board
    :param colour: colour of player who placed outflanking token
    :param coords: coordinates of placed token
    :return: return the updated board
    :rtype: list
    """
    size = len(board)
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:

            # Skip if no dx or dy
            if dx == dy and dx == 0:
                continue

            cur_coords = [coords[0] + dx, coords[1] + dy]
            line_coords = []
            flip_line = False

            while 0 <= cur_coords[0] < size and 0 <= cur_coords[1] < size:
                cur_token = board[cur_coords[1]][cur_coords[0]]
                if cur_token is None:
                    break

                elif cur_token == colour:
                    flip_line = True
                    break

                line_coords.append(cur_coords.copy()) # prevent just same thing being appended
                cur_coords[0] += dx
                cur_coords[1] += dy

            if flip_line and line_coords:
                for x, y in line_coords:
                    board[y][x] = colour

    return board

def has_legal_move(board, colour) -> bool:
    """
    Check if there is a possible move for a given player
    
    :param board: 2D list representing board
    :param colour: string representing the player
    :return: boolean representing if the player has a possible move
    :rtype: bool
    """
    # count_checked = 0
    for x in range(len(board)):
        for y in range(len(board)):
            if board[y][x] is None:
                # count_checked += 1
                if legal_move(colour, (x,y), board):
                    return True
    # print(f"Counted {count_checked}, no legals")
    return False

def check_win(board:list) -> list:
    """
    Given a board, return the amount of counters each player has and who has won
    
    :param board: 2d array representing the board
    :type board: list
    :return: a list containing a tuple with scores (Light, black) and a winner
    :rtype: list
    """
    light_tokens, black_tokens = 0, 0
    for row in board:
        for cell in row:
            if cell == "Dark ":
                black_tokens += 1
            elif cell == "Light":
                light_tokens += 1

    winner = None
    if black_tokens > light_tokens:
        winner = "Dark "
    elif light_tokens > black_tokens:
        winner = "Light"
    else:
        winner = "Draw"

    return ((light_tokens, black_tokens), winner)

class GameState:
    """
    Class for storing game state details and utility for transfering to and from JSON
    (with typing because I miss java)
    """
    def __init__(self, board:list, cur_player:str, finished:bool=False) -> None:
        self.board = board
        self.cur_player = cur_player
        self.finished = finished

    def to_dict(self) -> dict:
        """
        Return instance information as a dictionary
        """
        return {
            "board" : self.board,
            "cur_player" : self.cur_player,
            "finished" : self.finished
        }

    @classmethod # Not to do with the instance: to do with the class.
    def from_dict(cls: type["GameState"], data:dict) -> "GameState":
        """
        Initialise GameState class from dictionary data to allow for loading JSON saves
        
        :param cls: class for data to be loaded into
        :param data: dictionary
        """
        return cls(data["board"], data["cur_player"], data["finished"])

def simple_game_loop() -> None:
    """
    Simple game loop for intermediate manual testing through CLI
    """
    # Start the game with a welcome message:
    print( "#" * 27 + "\n" + "#" + " Welcome to Othello game " +"#" + "\n"+ "#" * 27 )

    # Initialise variables for game
    cur_board = initialise_board()
    move_counter = 60
    while move_counter > 0:
        # Check which players have possible moves
        black_has_legal = has_legal_move(cur_board, "Dark ")
        light_has_legal = has_legal_move(cur_board, "Light")
        # If neither player has possible turns, quit the loop:
        if not (black_has_legal or light_has_legal):
            break
        # By default, Dark goes first:
        if move_counter % 2 == 0 and black_has_legal:
            cur_player = "Dark "
        else:
            cur_player = "Light"

        # Display info to CLI
        print_board(cur_board)
        print(f"{move_counter} turns left\n{cur_player} is up")
        for x1 in range(8):
            for y1 in range(8):
                if legal_move(cur_player, (x1,y1), cur_board):
                    print(f"({y1}, {x1}) legal for {cur_player}")

        # Get current player to make their move:
        move_made = False
        while not move_made:
            move_coords = cli_coords_input()
            move_possible = legal_move(cur_player, move_coords, cur_board)
            if move_possible:
                print("Move is possible")
                cur_board[move_coords[1]][move_coords[0]] = cur_player
                cur_board = outflanked(cur_board, cur_player, move_coords)
                move_made = True
            else:
                print("Invalid move")
        move_counter -= 1

    # Game is over
    check_winner = check_win(cur_board)
    if check_winner[1] != "Draw":
        print(f"{check_winner[1]} has won {check_winner[0][0]}:{check_winner[0][1]}")
    else:
        print(f"Draw at {check_winner[0][0]}!")

if __name__ == "__main__":
    simple_game_loop()
