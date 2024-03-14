import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# users table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, salt TEXT)")

# insert data 
users_data = [('bsea', 'PANDAS!', 'BAMBOO'), ('fern', 'Gully', 'mooses'), 
              ('brakeman', 'mental', 'mices'), ('andy', 'ateapples', 'Battle')]
cursor.executemany("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", users_data)

# make th profiles table
cursor.execute('''CREATE TABLE IF NOT EXISTS profiles 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   userid INTEGER, 
                   color TEXT, 
                   hand TEXT, 
                   dept TEXT, 
                   "group" INTEGER DEFAULT 5)''')

# insert data assuming userID corresponds to the order of insertions above (idk if this is like bad coding practice)
profiles_data = [(2, 'red', 'right', 'math', 20), (1, 'green', 'right', 'math', 22), 
                 (4, 'purple', 'ambi', 'english', 12), (3, 'red', 'left', 'science', 5)]  

cursor.executemany("INSERT INTO profiles (userid, color, hand, dept, \"group\") VALUES (?, ?, ?, ?, ?)", profiles_data)


# printing results
print("Select color, dept from profiles:")
cursor.execute("SELECT color, dept FROM profiles")
for row in cursor.fetchall():
    print('\t'.join(map(str, row)))

print("\nSelect all columns where the hand is 'right':")
cursor.execute("SELECT * FROM profiles WHERE hand = 'right'")
for row in cursor.fetchall():
    print('\t'.join(map(str, row)))

print("\nSelect all columns where the password length is greater than 6 characters and they are right-handed:")
cursor.execute('''SELECT users.*, profiles.* 
                  FROM users 
                  JOIN profiles ON users.id = profiles.userid 
                  WHERE LENGTH(users.password) > 6 AND profiles.hand = 'right' ''')
for row in cursor.fetchall():
    print('\t'.join(map(str, row)))

print("\nSelect all usernames whose salt starts with B and group is over 10; they must be ordered alphabetically:")
cursor.execute('''SELECT username 
                  FROM users 
                  JOIN profiles ON users.id = profiles.userid 
                  WHERE salt LIKE 'B%' AND "group" > 10 
                  ORDER BY username''')
for row in cursor.fetchall():
    print('\t'.join(map(str, row)))

# commit changes and close  connection
conn.commit()
conn.close()
