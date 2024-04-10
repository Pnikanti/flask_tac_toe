from flask import Flask, send_from_directory, request

app = Flask(__name__)

tiles = [False for i in range(9)]

@app.route("/")
def main():
    return send_from_directory("static", "index.html")

@app.route("/api")
def api():
    id = request.args.get("id")

    if not id:
        return "No can do cowboy!"
    
    id = int(id)

    if (tiles[id]):
        return "Tile already clicked fool!"
    
    tiles[id] = True

    return str(id)