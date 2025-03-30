from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize Database
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    print("Database Initialized")

init_db()

# Route: Index Page (Now requires login)
@app.route('/')
@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html', username=session['user'])  # Show index with username
    return redirect(url_for('login'))  # Redirect to login if not logged in

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('index'))  # Redirect to index after login
        else:
            return "Invalid Credentials! Try again."

    return render_template('login.html')

# Route: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except:
            return "Username already exists!"

    return render_template('register.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))  # Redirect to login after logout

@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html', username=session['user'])
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
