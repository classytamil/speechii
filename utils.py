# utils.py
import sqlite3
import bcrypt
from datetime import datetime
import pytz

DB_PATH = "users.db"

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "fr": "French",
    "es": "Spanish"
}
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        username TEXT,
        password_hash TEXT,
        role TEXT DEFAULT 'user')''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        language TEXT,
        speed TEXT,
        filename TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_user(email, username, password, role='user'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users (email, username, password_hash, role) VALUES (?, ?, ?, ?)",
              (email, username, hashed_pw, role))
    conn.commit()
    conn.close()

def verify_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, username, role FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True, result[1], result[2]
    return False, None, None

def save_history(username, text, lang, speed, filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO history (username, text, language, speed, filename) VALUES (?, ?, ?, ?, ?)",
              (username, text, lang, speed, filename))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text, language, speed, filename, timestamp FROM history WHERE username = ? ORDER BY timestamp DESC", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT email, username, role FROM users")
    return c.fetchall()

def get_all_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, text, language, speed, timestamp FROM history ORDER BY timestamp DESC")
    return c.fetchall()

def get_tamilnadu_time():
    tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

def delete_history_entry(entry_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE id = ? AND username = ?", (entry_id, username))
    conn.commit()
    conn.close()
