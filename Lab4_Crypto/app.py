from flask import Flask, redirect, send_file, jsonify, render_template, request
import json 

app = Flask(__name__)


@app.route('/crypto/symmetric', methods=['GET'])
def get_form():
    """
    Redirects to the Cryptography Form page.

    Returns:
        Response: Flask Response object.
    """
    
    return render_template('./crypto/symmetric.html')


@app.route('/crypto/symmetric', methods=['POST'])
def symmetric_crypto():
    """
    Handles POST requests from symmetric ciphers to encrypt or decrypt data. 

    Returns:
        Response: SUCCESS string and HTTP status 200.
    """
    cipher = request.form.get('cipher')
    mode = request.form.get('action')
    message = request.form.get('message')
    password = request.form.get('password')

    # Add logic to perform encryption or decryption based on user's choices (cipher, mode, message, and password)
    return crypto_logic(cipher, mode, message, password)


"""
    Handles cryptography logic for both Vigenere and Ceasar Ciphers

    Returns:JSON-Encoded string containing either the successful encryption or decryption of 
            the cipher, or an Invalid Character error with the keycode. 
"""
def crypto_logic(cipher, mode, message, password):    
     #Checks if all keys have keycodes between 32 and 126
     #Returns: True/False depending on above condition
     def is_printable(char):
        return 32 <= ord(char) <= 126

    # logic for encrypting and decrypting Vigenere cipher
    # Params: char -- message characters
    #         key_char -- password characters
    #         mode -- encrypt/decrypt
    #It does one character at a time -- preforms a mini ceasar type thing :)
     def vigenere_transform(char, key_char, mode):
        char_code = ord(char)
        key_code = ord(key_char) # gets char value of password character
        operation = (1 if mode == "encrypt" else -1) #max showed me this slick method
        transformed_char_code = ((char_code - 32 + operation * (key_code - 32)) % 95) + 32 #mini ceasar
        return chr(transformed_char_code)
    
    

     if cipher == "caesar":
        result = ""
        for char in message:
            if not is_printable(char): #catch
                return json.dumps({"status": "error", "message": f"INVALID CHARACTER: {ord(char)}"}) 
            if mode == "encrypt":
                shifted_char = chr(((ord(char) - 32 + int(password)) % 95) + 32) #shifts
            elif mode == "decrypt":
                shifted_char = chr(((ord(char) - 32 - int(password)) % 95) + 32) #shifts
            result += shifted_char
        if mode == "encrypt": 
            return json.dumps({"status": "encrypt", "message": result})
        elif mode == "decrypt":
            return json.dumps({"status": "decrypt", "message": result})
        
     elif cipher == "vigenere":
        encrypted_text = ""
        for i, char in enumerate(message):
            if not is_printable(char): #catch
                return json.dumps({"status": "error", "message": f"INVALID CHARACTER: {ord(char)}"})
            key_char = password[i % len(password)] #find wich character in password to shift by
            shifted_char = vigenere_transform(char, key_char, mode)
            encrypted_text += shifted_char
        print(encrypted_text) # for some reason (i think it is something to do with how html handles characters)
                              # this encrypted version is correct, but the one displayed in the JSON is not 
                              # always correct so use this for decryption...
        return json.dumps({"status": mode, "message": encrypted_text})
     else:
        return json.dumps({"status": "error", "message": "Invalid cipher type"})




@app.route('/crypto/steg', methods=['GET'])
def steg_form():
    """
    Redirects to the Steganography Form page.

    Returns:
        Response: Flask Response object.
    """
    return render_template('./crypto/steg.html')


@app.route('/crypto/steg', methods=['POST'])
def steg_crypto():
    """
    Handles POST requests from steg to encrypt or decrypt photos. 

    Returns:
        Response: SUCCESS string and HTTP status 200.
    """
    host_image = request.files['host_image']
    steg_mode = request.form.get("message_type")
    if steg_mode == "text":
        client_message = request.form.get('client_message')
    else:
        client_message = request.files['client_image']

    # Add logic to perform steganography based on user's choices
    result = steg_logic(host_image, client_message, steg_mode)
    print(result)
    return "SUCCESS", 200

def steg_logic(host_image, client_message, steg_mode):
    """
    Handles steg logic. 

    Returns: Encrypted or Decrypted steg. (I don't know if thats what its called)
    """
    return host_image, client_message, steg_mode #placeholder












# Divider
# Divider
# SERVER LAB2 STUFF 
# Divider
# Divider

@app.route('/', methods = ["GET"]) # I forgot this line on my lab2 I think :'( 
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
    