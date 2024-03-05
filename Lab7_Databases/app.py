from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    mode = request.form['mode']
    print(username, password, mode)
    return "SUCCESS"

@app.route('/logout', methods=['POST'])
def logout():
    return "SUCCESS"

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

@app.route('/profile', methods=['POST'])
def handle_profile():
    action = request.form['action']
    # Print all received fields for debugging
    print(action, request.form)
    return "SUCCESS"

@app.route('/files', methods=['POST'])
def handle_files():
    action = request.form['action']
    print(action, request.form)
    return "SUCCESS"

if __name__ == "__main__":
    app.run(port=8022)
