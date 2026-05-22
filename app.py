import sqlite3
import hashlib
from flask import Flask, request, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_portfolio_key'

SECURITY_ENABLED = False

def get_db_connection():
    conn = sqlite3.connect('bank.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/toggle-security', methods=['POST'])
def toggle_security():
    global SECURITY_ENABLED
    SECURITY_ENABLED = not SECURITY_ENABLED
    state = "ENABLED" if SECURITY_ENABLED else "DISABLED"
    print(f"[*] Security is now {state}")
    return redirect(request.referrer or url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        if not SECURITY_ENABLED:
            query = f"SELECT * FROM users WHERE username = '{username}' AND plaintext_password = '{password}'"
            try:
                cursor.execute(query)
                user = cursor.fetchone()
            except sqlite3.OperationalError as e:
                return f"Database Error (SQL Injection triggered this!): {e}", 500
        else:
            secure_hash = hashlib.sha256(password.encode()).hexdigest()
            query = "SELECT * FROM users WHERE username = ? AND hashed_password = ?"
            cursor.execute(query, (username, secure_hash))
            user = cursor.fetchone()
            
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard', id=user['id']))
        
        return "Invalid credentials", 401
        
    return render_template('login.html', security_mode=SECURITY_ENABLED)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    requested_id = request.args.get('id')
    logged_in_id = session.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if not SECURITY_ENABLED:
        cursor.execute("SELECT name, balance FROM users WHERE id = ?", (requested_id,))
    else:
        if str(requested_id) != str(logged_in_id):
            conn.close()
            return "⛔ Access Denied: Unauthorized Access Attempt Logged!", 403
        cursor.execute("SELECT name, balance FROM users WHERE id = ?", (logged_in_id,))

    account_data = cursor.fetchone()
    conn.close()
    
    if not account_data:
        return "Account not found", 404

    return render_template('dashboard.html', account=account_data, security_mode=SECURITY_ENABLED, current_id=requested_id)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        author = session.get('username', 'Anonymous')
        text = request.form['comment_text']
        cursor.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (author, text))
        conn.commit()

    cursor.execute("SELECT author, text FROM comments")
    all_comments = cursor.fetchall()
    conn.close()

    if not SECURITY_ENABLED:
        return render_template('comments_vulnerable.html', comments=all_comments, security_mode=SECURITY_ENABLED)
    else:
        return render_template('comments_secure.html', comments=all_comments, security_mode=SECURITY_ENABLED)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)