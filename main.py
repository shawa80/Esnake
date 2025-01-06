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

def look(blocked: set[Corr], food: set[Corr], danger: set[Corr], loc: Corr) -> int:
    score = 0
    weight1 = 128
    weight2 = 32
    foodWeight = 10

    if loc not in blocked:
        if loc in danger:
            score += (weight1/2)
        else:
            score += weight1

    print(f"*loc check {score}")

    if score == 0:
        return 0

    if loc.left() not in blocked:
        if loc.left() in danger:
            score += weight2/2
        else:
            score += weight2

    if loc.right() not in blocked: 
        if loc.right() in danger:
            score += weight2/2
        else:
            score += weight2

    if loc.up() not in blocked:
        if loc.up() in danger:
            score += weight2/2
        else:
            score += weight2

    if loc.down() not in blocked: 
        if loc.down() in danger:
            score += weight2/2
        else:
            score += weight2
    
    print(f"area check {score}")

    
    print(f"food check {score}")

    #if we have two exits, increase food weight
    if score == (weight1 + weight2 + weight2):
        foodWeight = weight2 + 1

    if loc in food:
        score += foodWeight

    if loc.left() in food:
        score += foodWeight
    if loc.right() in food: 
        score += foodWeight
    if loc.up() in food:
        score += foodWeight
    if loc.down() in food: 
        score += foodWeight

    print(f"area food check {score}")
    return score

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    print(f"turn {game_state['turn']}")

    blocked = set()
    food = set()
    snakeDanger = set()
    is_move_safe = {"up": 0, "down": 0, "left": 0, "right": 0}

    my_head = Corr.fromObj(game_state["you"]["body"][0])  # Coordinates of your head
    my_health = game_state["you"]["health"]
    my_length = len(game_state["you"]["body"])
    my_id = game_state["you"]["id"]

    for s in game_state["board"]["snakes"]:
        if len(s["body"]) >= my_length and s["id"] != my_id:
            d = Corr.fromObj(s["head"])
            snakeDanger.add(d.left())
            snakeDanger.add(d.right())
            snakeDanger.add(d.up())
            snakeDanger.add(d.down())

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

    is_move_safe["left"] = look(blocked, food, snakeDanger, my_head.left());
    is_move_safe["right"] = look(blocked, food, snakeDanger, my_head.right());
    is_move_safe["up"] = look(blocked, food, snakeDanger, my_head.up());
    is_move_safe["down"] = look(blocked, food, snakeDanger, my_head.down());


    highest = sorted(is_move_safe.items(), key=lambda item: item[1], reverse=True)
    print(highest)
    (next_move, score) = highest[0]

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# # Start server when `python main.py` is run
# if __name__ == "__main__":
#     from server import run_server

#     run_server({"info": info, "start": start, "move": move, "end": end})
