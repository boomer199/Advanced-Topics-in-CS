from flask import Flask, redirect, send_file, jsonify, render_template, request

app = Flask(__name__)


def home():
    """
    Redirects to the portfolio page.

    Returns:
        Response: Flask Response object.
    """
    return redirect("./static/index.htm")

@app.route("/minesweeper", methods=['GET'])
def minesweeper():
    """
    Redirects to the Minesweeper introduction page.

    Returns:
        Response: Flask Response object.
    """
    return redirect("./minesweeper/intro.html")

@app.route("/minesweeper/<path:path>", methods=['GET'])
def mine_file(path):
    """
    Serves Minesweeper game files.

    Args:
        path (str): The path to the game file.

    Returns:
        Response: Flask Response object with the game file.
    """
    return send_file("./minesweeper/" + path)

# Data structure to store completed games
completed_games = []

# Data structure to store player statistics
player_stats = {}

@app.route("/minesweeper", methods=["POST"])
@app.route("/minesweeper/minesweeper.html", methods=["POST"])
def complete_game():
    """
    Handles POST requests to save game data and update player statistics.

    Returns:
        Response: Flask Response object with a success message and HTTP status 200.
    """
    # Extract game data from the POST request
    data = request.get_json()

    # Extract individual game data fields
    name = data.get("name")
    rows = data.get("rows")
    columns = data.get("columns")
    difficulty = data.get("difficulty")
    covered_spaces = data.get("covered_spaces")
    score = data.get("score")
    win_loss = data.get("win")
    time = data.get("time")

    # Add game data to the list of completed games
    completed_games.append({
        "name": name,
        "rows": rows,
        "columns": columns,
        "difficulty": difficulty,
        "covered_spaces": covered_spaces,
        "score": score,
        "win_loss": win_loss,
        "time": time
    })
    print(completed_games)

    # Update player stats dictionary
    if name in player_stats:
        player_stats[name]["games_played"] += 1
        if win_loss == True:
            player_stats[name]["wins"] += 1
        elif win_loss == False:
            player_stats[name]["loses"] += 1
        player_stats[name]["total_time"] += time
        player_stats[name]["total_score"] += score
    else:
        player_stats[name] = {
            "games_played": 1,
            "wins": 1 if win_loss == "win" else 0,
            "loses": 1 if win_loss == "loss" else 0,
            "total_time": time,
            "total_score": score
        }

    # Respond with a success message and HTTP status 200
    return jsonify({"message": "Game data saved successfully"}), 200

@app.route("/minesweeper/leaders", methods=["GET"])
def leaderboard():
    """
    Generates and displays the leaderboard.

    Returns:
        Response: Flask Response object with the leaderboard data.
    """
    # Calculate computed ranking for each player
    leader_data = []
    for name, stats in player_stats.items():
        wins = stats["wins"]
        loses = stats["loses"]
        total_time = stats["total_time"]
        total_score = stats["total_score"]
        games_played = stats["games_played"]

        # Calculate the computed ranking for each player
        if wins + loses == 0:
            computed_ranking = 0
        else:
            computed_ranking = (wins / (wins + loses)) * (total_time / games_played) * (total_score / games_played)

        leader_data.append({
            "name": name,
            "wins": wins,
            "loses": loses,
            "average_time": total_time / games_played,
            "average_score": total_score / games_played,
            "computed_ranking": computed_ranking
        })

    # Sort the leaderboard by computed ranking in descending order
    sorted_leaderboard = sorted(leader_data, key=lambda x: x["computed_ranking"], reverse=True)

    # Render the leaderboard template with the sorted leaderboard data
    return render_template("leaderboard.html", leaderboard=sorted_leaderboard)

if __name__ == "__main__":
    app.run(debug=True, port=4242)
    