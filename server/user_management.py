import sqlite3
import bcrypt

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect("user_db.db")
cursor = conn.cursor()

# Create a table to store user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Commit the changes and close the database connection
conn.commit()

# Function to register a new user
def register_user(username, password):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the user's data into the table
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# Function to authenticate a user
def authenticate_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()

    if row:
        # Compare the provided password with the hashed password in the database
        if bcrypt.checkpw(password.encode(), row[0]):
            return True

    return False

# Close the database connection when done
conn.close()
