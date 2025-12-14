"""
Module containing flask logic
"""

import json
import os

from flask import Flask, render_template, request
from components import initialise_board, legal_move, print_board
from game_engine import GameState, outflanked, has_legal_move, check_win
from ai_opponent import number_flipped, possible_flip_counts, choose_move

app = Flask(__name__)

@app.route("/")
def index():
    """
    Ran when the user first opens the page. 
    Load the game, and present it to the user.
    """
    # board = initialise_board()
    # return render_template("board.html", game_board=board)
    global game_state

    try:
        if game_state.finished:
            os.remove("game_state.json")
    except NameError:
        pass
    # If we don't already have a game_state.json file make one:
    if not os.path.exists("game_state.json"):
        game_state = GameState(board=initialise_board(), cur_player="Dark ")
        with open("game_state.json", "w", encoding="UTF-8") as f:
            json_str = json.dumps(game_state.to_dict(), indent=4)
            f.write(json_str)

    # If it does exist, load the game state
    elif os.path.exists("game_state.json"):
        with open("game_state.json", "r", encoding="UTF-8") as f:
            game_state = GameState.from_dict(json.load(f))

    print_board(game_state.board)

    return render_template(
        "board.html",
        game_board=game_state.board,
        cur_player = game_state.cur_player
    )


@app.route("/move", methods=["GET", "POST"])
def move():
    """
    Where the user has made a move, update game state if it's a legal move. 
    Then get the AI to make a move. Update game state, and pass back to player.
    """
    x = request.args.get("x", type=int)
    y = request.args.get("y", type=int)

    # If the requested move is legal:
    if legal_move(game_state.cur_player, (x,y), game_state.board):
        # Store how many tokens the move flips
        move_flips = number_flipped(game_state.board, game_state.cur_player, (x,y))
        # Mutate board
        game_state.board[y][x] = game_state.cur_player
        game_state.board = outflanked(game_state.board, game_state.cur_player, (x,y))

        # Check who can go
        dark_has_legal = has_legal_move(game_state.board, "Dark ")
        light_has_legal = has_legal_move(game_state.board, "Light")

        # AI takes a move if it can
        if light_has_legal:
            # AI takes its turn
            ai_move = choose_move(move_flips, possible_flip_counts(game_state.board, "Light"))
            game_state.board[ai_move[1]][ai_move[0]] = "Light"
            game_state.board = outflanked(game_state.board, "Light", ai_move)

        # Make the AI go until it's not their turn anymore
        while True:
            # Calculate legal moves
            dark_has_legal = has_legal_move(game_state.board, "Dark ")
            light_has_legal = has_legal_move(game_state.board, "Light")

            # Game ends if neither player can go
            if not dark_has_legal and not light_has_legal:
                print("Game is finished")
                check_winner = check_win(game_state.board)
                if check_winner[1] != "Draw":
                    message = f"{check_winner[1]} has won {check_winner[0][0]}:{check_winner[0][1]}"
                else:
                    message = f"Draw at {check_winner[0][0]}!"
                game_state.finished = True
                message = message + "\nRefresh to start new game"
                return {
                    "status" : "n/a",
                    "player" : "n/a",
                    "board" : game_state.board,
                    "finished" : message
                }

            if light_has_legal and not dark_has_legal:
                # AI takes its turn
                ai_move = choose_move(move_flips, possible_flip_counts(game_state.board, "Light"))
                game_state.board[ai_move[1]][ai_move[0]] = "Light"
                game_state.board = outflanked(game_state.board, "Light", ai_move)
                continue # Go back to top of while True to recheck game state

            break

        # Update the json file
        with open("game_state.json", "w", encoding="UTF-8") as f:
            json_str = json.dumps(game_state.to_dict(), indent=4)
            f.write(json_str)

        # Return statement:
        return {
            "status" : "success",
            "finished" : game_state.finished,
            "board" : game_state.board,
            "player" : game_state.cur_player
        }

    # If the move is illegal:
    message = None
    # No changes to make - based on why move is illegal
    if game_state.board[y][x] is not None:
        message = "Cell already occupied"
    else:
        message = "No outflanked peices"

    return {
        "status" : "fail",
        "finished" : game_state.finished,
        "board" : game_state.board,
        "player" : game_state.cur_player,
        "message" : message
    }
