import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    print("[*] Initializing database...")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            plaintext_password TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM comments")

    print("[*] Inserting mock users and comments...")
    
    admin_pass = "SuperSecretAdmin123!"
    cursor.execute('''
        INSERT INTO users (username, plaintext_password, hashed_password, name, balance)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', admin_pass, hash_password(admin_pass), 'Bruce Wayne', 750000.00))

    user_pass = "password123"
    cursor.execute('''
        INSERT INTO users (username, plaintext_password, hashed_password, name, balance)
        VALUES (?, ?, ?, ?, ?)
    ''', ('victim_user', user_pass, hash_password(user_pass), 'Peter Parker', 45.50))

    cursor.execute('''
        INSERT INTO comments (author, text)
        VALUES (?, ?)
    ''', ('John Doe', 'Hey everyone! This banking app looks awesome.'))

    cursor.execute('''
        INSERT INTO comments (author, text)
        VALUES (?, ?)
    ''', ('Hacker99', '<script>alert("XSS Vulnerability Proven! session_id: " + document.cookie)</script>'))

    conn.commit()
    conn.close()
    print("[+] Database successfully created and populated as 'bank.db'!")

if __name__ == '__main__':
    initialize_database()