"""
Module containing flask logic
"""

import json
import os

from flask import Flask, render_template, request
from components import initialise_board, legal_move, print_board
from game_engine import GameState, outflanked, has_legal_move

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
    Where the user has made a move, update game state if it's a legal move
    """
    x = request.args.get("x", type=int)
    y = request.args.get("y", type=int)

    # If the requested move is legal:
    if legal_move(game_state.cur_player, (x,y), game_state.board):
        # Mutate board
        game_state.board[y][x] = game_state.cur_player
        game_state.board = outflanked(game_state.board, game_state.cur_player, (x,y))

        # Change the current player
        dark_has_legal = has_legal_move(game_state.board, "Dark ")
        light_has_legal = has_legal_move(game_state.board, "Light")

        # If neither player has possible moves, the game is done
        if not (dark_has_legal or light_has_legal):
            game_state.finished = True

        if game_state.cur_player == "Dark " and light_has_legal:
            game_state.cur_player = "Light"
        else:
            game_state.cur_player = "Dark "

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
    else:
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
