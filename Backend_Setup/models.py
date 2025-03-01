from flask_bcrypt import Bcrypt
import sqlite3

bcrypt = Bcrypt()

def create_tables():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            credits INTEGER DEFAULT 20
        )
    ''')

    conn.commit()
    conn.close()

def register_user(username, password, role="user"):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
        print(f"User {username} registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    
    conn.close()
