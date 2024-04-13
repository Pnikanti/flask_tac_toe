from flask import Flask, send_from_directory, request, jsonify
from numbers import Number

app = Flask(__name__)
games = []

class Game:
    def __init__(self, id):
        self.tiles = [None for i in range(9)]
        self.players = []
        self.id = id
        self.turn = None

##### ENDPOINTS #####

@app.route("/")
def main():
    return send_from_directory("static", "index.html")
    
@app.route("/api/tick")
def tick():
    game_id = request.args.get("gameId")
    tile_id = request.args.get("tileId")
    player_id = request.args.get("playerId")
    
    if not game_id:
        return jsonify({
            "statusText":  "Game ID must be specified!",
            "success": False
        })
    
    if not tile_id:
        return jsonify({
            "statusText":  "Tile ID must be specified!",
            "success": False
        })
    
    if not player_id:
        return jsonify({
            "statusText":  "Player ID must be specified!",
            "success": False
        })
    
    tile_id = int(tile_id)

    return tick_game(game_id, player_id, tile_id)

@app.route("/api/register")
def register():
    game_id = request.args.get("gameId")
    player_id = request.args.get("playerId")
    
    if not game_id:
        return jsonify({
            "statusText":  "Game ID must be specified!",
            "success": False
        })
    
    if not player_id:
        return jsonify({
            "statusText":  "Player ID must be specified!",
            "success": False
        })
    
    return player_register(game_id, player_id)

@app.route("/api/get")
def get():
    game_id = request.args.get("gameId")

    if not game_id:
        return jsonify({
            "statusText":  "Game ID must be specified!",
            "success": False
        })
    
    game_id = int(game_id)
    
    return get_game(game_id)

@app.route("/api/new")
def new():
    return new_game()

##### BIZ LOGIC ######

def tick_game(game_id, player_id, tile_id):
    game_id = parse_game_id(game_id)
    
    if not isinstance(game_id, Number):
        return game_id
    
    game: Game = games[game_id]

    tile_id = int(tile_id)
    
    if tile_id > len(games[game_id].tiles):
        return jsonify({
            "statusText": f"Tile ID {tile_id} was not found!",
            "success": False
        })
    
    if player_id not in game.players:
        return jsonify({
            "statusText": f"Player ID {player_id} was not registered to the game!",
            "success": False
        })

    if game.tiles[tile_id]:
        return jsonify({
            "statusText":  "Tile already clicked!",
            "success": False
        })
    
    game.tiles[tile_id] = True

    return jsonify({
        "statusText":  "Game tick!",
        "success": True
    })
    
def reset_game(game_id):
    game_id = parse_game_id(game_id)
    
    if not isinstance(game_id, Number):
        return game_id
    
    games[game_id].tiles = [None for i in range(9)]
    games[game_id].players = []

    return jsonify({
        "statusText":  "Game Reset!",
        "success": True
    })

def get_game(game_id):
    game_id = parse_game_id(game_id)
    
    if not isinstance(game_id, Number):
        return game_id
    
    game: Game = games[game_id]

    return jsonify({
        "statusText": f"Game state retrieval successful",
        "success": True,
        "state": {
            "id": game.id,
            "tiles": game.tiles,
            "turn": game.turn,
            "players": game.players
        }
    })

def new_game():
    game_id = len(games)
    games.append(Game(game_id))

    return jsonify({
        "statusText": f"Created a new game with ID: {games[game_id].id}",
        "success": True,
        "id": games[game_id].id
    })

def player_register(game_id, player_id):
    game_id = parse_game_id(game_id)
    
    if not isinstance(game_id, Number):
        return game_id
    
    game: Game = games[game_id]

    if len(game.players) >= 2:
        return jsonify({
            "statusText":  f"Player limit exceeded!",
            "success": False
        })
    
    game.players.append(player_id)

    return jsonify({
        "statusText":  f"Registered player with ID: {player_id}",
        "success": True
    })
    
def parse_game_id(game_id) -> int:
    game_id = int(game_id)

    if len(games) <= game_id:
        return jsonify({
            "statusText":  f"Game with ID: {game_id} not found!",
            "success": False
        })
    
    if not games[game_id]:
        return jsonify({
            "statusText":  f"Game with ID: {game_id} not found!",
            "success": False
        })
    
    return game_id