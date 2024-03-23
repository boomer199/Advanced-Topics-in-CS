from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib 
from db import get_db, close_db, init_db, query_db
import sqlite3
import uuid
import os
import random
import string
import redis

redis_client = redis.Redis(host='localhost', port=6379) #redis on default port


app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'db.db') # getcwd method returns the current working directory

app.secret_key = os.urandom(24)

with app.app_context():
    init_db()

def generate_salt(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def hash_password(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

@app.before_request
def before_request():
    get_db()
    user_id = session.get('user_id')
    user_session_uuid = session.get('user_session_uuid')

    if user_id and user_session_uuid:
        # Retrieve the session UUID from Redis using the user's identifier
        valid_session_uuid = redis_client.get(f"user_session:{user_id}")
        
        if not valid_session_uuid or valid_session_uuid.decode() != user_session_uuid:
            # If there's no matching UUID in Redis or they don't match, session is invalid
            session.clear()  # Clears the entire session
            # Redirect to login or take other appropriate action

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

from flask import Flask, redirect, url_for, session

@app.route('/')
def default():
    # Check if a user is logged in by looking for a unique identifier in the session
    if 'user_id' in session:
        # If logged in, redirect to the user's profile page
        # Assuming you store the user's username as the identifier in session['username']
        # Adjust according to your session management strategy
        return redirect(url_for('profile', user=session['username']))
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))



@app.route('/register', methods=['POST'])
def register():
    # Extract form data
    username = request.form['username']
    password = request.form['password']
    
    # Generate a new salt and hash the password
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    
    try:
        db = get_db()
        # Insert the new user into the accounts table
        cursor = db.execute('INSERT INTO accounts (username, password, salt) VALUES (?, ?, ?)', 
                            (username, hashed_password, salt))
        new_user_id = cursor.lastrowid  # Get the ID of the newly created user

        # Create a corresponding profile for the new user
        # Assuming default values for fname, lname, avatar, and files, adjust as necessary
        db.execute('INSERT INTO profiles (userid, fname, lname, avatar, files) VALUES (?, ?, ?, ?, ?)', 
                   (new_user_id, 'Default', 'User', 'default_avatar.png', 'default_files_path'))
        
        db.commit()
        flash("Registration successful. Please log in.")
    except sqlite3.IntegrityError as e:
        db.rollback()
        flash('An error occurred: ' + str(e))
    
    return redirect(url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mode = request.form.get('mode')

        if mode == "register":
            existing_user = query_db('SELECT * FROM accounts WHERE username = ?', [username], one=True)
            if existing_user:
                flash("Username already exists.")
                return render_template('login.html')
            
            salt = generate_salt()  # Generate a new salt for this user
            hashed_password = hash_password(password, salt)  # Hash the password with the salt
            
            try:
                get_db().execute('INSERT INTO accounts (username, password, salt) VALUES (?, ?, ?)', 
                                 (username, hashed_password, salt))
                get_db().commit()
            except sqlite3.IntegrityError as e:
                flash('An error occurred: ' + str(e))
                return redirect(url_for('login'))

            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))

        elif mode == "login":
            user = query_db('SELECT * FROM accounts WHERE username = ?', [username], one=True)
            if user:
                # Hash the provided password with the user's salt and compare it to the stored hash
                hashed_input_password = hash_password(password, user['salt'])
                if hashed_input_password == user['password']:
                    session['user_id'] = user['rowid']
                    user_session_uuid = str(uuid.uuid4())
                    session['user_session_uuid'] = user_session_uuid
                    redis_client.set(f"user_session:{user['rowid']}", user_session_uuid, ex=3600)  #expiry time for the session key (3600 seconds = 1hr)
                    return redirect(url_for('profile', user=username))
                else:
                    flash("Invalid username or password.")
            else:
                flash("Invalid username or password.")
    
    return render_template('login.html')



@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        # Delete the session UUID from Redis using the user's identifier
        redis_client.delete(f"user_session:{user_id}")

    # Clear the session
    session.clear()
    return redirect(url_for('login'))
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/<user>/profile', methods=['GET', 'POST'])
def profile(user):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_data = query_db('SELECT * FROM profiles WHERE userid = ?', [session['user_id']], one=True)
    if not user_data:
        flash("Profile not found.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if request.form.get('action') == 'logout':
            return redirect(url_for('logout'))
        # Add more conditions here for updating password, picture, etc.
    
    user_data = query_db('SELECT * FROM profiles WHERE userid = ?', [session['user_id']], one=True)
    if not user_data:
        flash("Profile not found.")
        return redirect(url_for('login'))
    return render_template('profile.j2', profile=user_data)

if __name__ == "__main__":
    app.run(port=8022, debug=True)
