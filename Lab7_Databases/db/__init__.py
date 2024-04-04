import os, json, sqlite3, redis, hashlib, random, uuid, shutil
from .models import Account, Profile

REDIS_PORT, DB_FILE = 6379, "db.db"
ASCII_VALID_RANGE = list(range(48, 58)) + list(range(97, 123))
SALT_LEN = 10

sqlite_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
redis_server = redis.Redis(host="localhost", port=REDIS_PORT, decode_responses=True)



def setup_db():
    """
    Creates the necessary SQLite tables if they don't exist
    """
    with sqlite_conn:
        cursor = sqlite_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT NOT NULL, password TEXT NOT NULL, salt VARCHAR(10) NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS profiles (userid INTEGER PRIMARY KEY, fname TEXT, lname TEXT, avatar TEXT, files TEXT);")
        
        
setup_db()

def password_encode(salt, password):
    """
    Mixes password with salt and hashes them because plain text passwords are a no-go zone.
    """
    return hashlib.sha256((salt + password).encode()).hexdigest()

def generate_salt():
    """
    Generates a random sequence to salt passwords... why is it called salting????
    """
    return ''.join(random.choice(chr(x)) for x in random.choices(ASCII_VALID_RANGE, k=SALT_LEN))

def account_create(username, password):
    """
    Creates a new account and profile, sets up a file directory for them .
    """
    salt, acc = generate_salt(), Account()
    acc.username, acc.password, acc.salt = username, password, salt
    
    prof, new_path = Profile(), os.path.join("static/files", username, "")
    files_path = os.path.join(os.getcwd(), new_path)
    prof.username, prof.files = username, new_path
    os.makedirs(files_path, exist_ok=True)
    
    with sqlite_conn:
        cur = sqlite_conn.cursor()
        cur.execute('INSERT INTO accounts (username, password, salt) VALUES (?, ?, ?)', (username, password_encode(salt, password), salt))
        uid = cur.lastrowid
        cur.execute('INSERT INTO profiles (userid, files) VALUES (?, ?)', (uid, files_path))
        
    return prof

def account_auth(username, password):
    """
    Checks if the username and password combo is valid
    """
    cur = sqlite_conn.cursor()
    
    try:
        cur.execute('SELECT password, salt FROM accounts WHERE username = ?', (username,))
        result = cur.fetchone()
        cur.close()  # manually close the cursor
        return bool(result) and result[0] == password_encode(result[1], password)
    
    except Exception as e:
        cur.close()  # make sure to close the cursor in case of an error
        raise e
    
    
def account_update_password(username, new_password):
    """
    Changes the user's password because change is good... sometimes
    """
    try:
        with sqlite_conn:
            cur = sqlite_conn.cursor()
            cur.execute('SELECT salt FROM accounts WHERE username = ?', (username,))
            salt = cur.fetchone()[0]
            cur.execute('UPDATE accounts SET password = ? WHERE username = ?', (password_encode(salt, new_password), username))
        return True
    
    except Exception:
        print("that didnt work")
        return False

def profile_update(token, username, fname=None, lname=None, avatar=None):
    """
    Updates profile info 
    """
    try:
        with sqlite_conn:
            cur = sqlite_conn.cursor()
            cur.execute('SELECT rowid FROM accounts WHERE username = ?', (username,))
            uid = cur.fetchone()[0]
            updates = [(fname, 'fname'), (lname, 'lname'), (avatar, 'avatar')]
            
            for value, column in updates:
                if value is not None:
                    cur.execute(f'UPDATE profiles SET {column} = ? WHERE userid = ?', (value, uid))
        profile = session_get(token)
        
        if profile:
            redis_server.set(token, str(profile))
            return True
        return False
    
    except Exception:
        return False

def profile_delete(username):
    try:
        with sqlite_conn:
            cur = sqlite_conn.cursor()
            cur.execute('SELECT rowid FROM accounts WHERE username = ?', (username,))
            uid = cur.fetchone()[0]
            cur.execute('SELECT avatar, files FROM profiles WHERE userid = ?', (uid,))
            avatar, files = cur.fetchone()
            cur.execute('DELETE FROM accounts WHERE username = ?', (username,))
            cur.execute('DELETE FROM profiles WHERE userid = ?', (uid,))
            
        if avatar: os.remove(os.path.join(os.getcwd(), avatar))
        if files: shutil.rmtree(files, ignore_errors=True)
        return True
    
    except Exception:
        return False

def session_set(profile):
    token = uuid.uuid4().hex
    redis_server.set(token, json.dumps(profile.jsonify()))
    return token

def session_get(token):
    profile_str = redis_server.get(token)
    
    if profile_str:
        info = json.loads(profile_str)
        prof = Profile()
        prof.username, prof.fname, prof.lname, prof.avatar, prof.files = info['username'], info.get('fname'), info.get('lname'), info.get('avatar'), info.get('files')
        return prof
    
    return None

def session_delete(token):
    try:
        redis_server.delete(token)
        return True
    except:
        return False

def profile_get(username):
    cur = sqlite_conn.cursor()
    cur.execute(f'select profiles.fname, profiles.lname, profiles.avatar, profiles.files from accounts inner join profiles on accounts.rowid = profiles.userid where accounts.username = "{username}";')
    
    fetched_results = cur.fetchall()

    if len(fetched_results) > 0:
        fname, lname, avatar, files = fetched_results[0]
    else:
        return None

    prof = Profile()
    prof.username = username
    prof.fname = fname
    prof.lname = lname
    prof.avatar = avatar
    prof.files = files

    return prof