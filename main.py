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

def look(blocked: set[Corr], food: set[Corr], loc: Corr) -> int:
    score = 0
    weight = 32
    foodWeight = 10

    if loc not in blocked:
        score += 128

    if loc in food:
        score += foodWeight

    if loc.left() not in blocked:
        score += weight
    if loc.right() not in blocked: 
        score += weight
    if loc.up() not in blocked:
        score += weight
    if loc.down() not in blocked: 
        score += weight

    if loc.left() in food:
        score += foodWeight
    if loc.right() in food: 
        score += foodWeight
    if loc.up() in food:
        score += foodWeight
    if loc.down() in food: 
        score += foodWeight

    return score

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    blocked = set()
    food = set()
    is_move_safe = {"up": 0, "down": 0, "left": 0, "right": 0}

    my_head = Corr.fromObj(game_state["you"]["body"][0])  # Coordinates of your head

    for f in game_state["board"]["food"]:
        food.add(Corr.fromObj(f))

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

    is_move_safe["left"] = look(blocked, food, my_head.left());
    is_move_safe["right"] = look(blocked, food, my_head.right());
    is_move_safe["up"] = look(blocked, food, my_head.up());
    is_move_safe["down"] = look(blocked, food, my_head.down());


    highest = sorted(is_move_safe.items(), key=lambda item: item[1], reverse=True)
    print(highest)
    (next_move, score) = highest[0]

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
