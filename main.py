# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

from corr import Corr


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "E-Snake",
        "color": "#bd0202",  
        "head": "silly",
        "tail": "nr-booster",  
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    blocked = set()
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = Corr.fromObj(game_state["you"]["body"][0])  # Coordinates of your head
    #my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    for body in game_state["you"]["body"]:
        blocked.add(Corr.fromObj(body))
    for snake in game_state["board"]["snakes"]:
        for body in snake["body"]:
            blocked.add(Corr.fromObj(body))
    height = game_state["board"]["height"]
    width = game_state["board"]["height"]
    for x in range(width):
        blocked.add(Corr(x, height))
        blocked.add(Corr(x, -1))
    for y in range(height) :
        blocked.add(Corr(-1, y))
        blocked.add(Corr(width, y))

    for b in blocked:
        print(f"blocks {b.x} {b.y}")

    if Corr(my_head.x-1, my_head.y) in blocked:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        print("left not safe")

    if Corr(my_head.x+1, my_head.y) in blocked:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        print("right not safe")

    if Corr(my_head.x, my_head.y-1) in blocked:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        print("down not safe")

    if Corr(my_head.x, my_head.y+1) in blocked:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        print("up not safe")

    # if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    #     is_move_safe["left"] = False

    # elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    #     is_move_safe["right"] = False

    # elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    #     is_move_safe["down"] = False

    # elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    #     is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
