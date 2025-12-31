import sqlite3
import secrets
import os

DB_PATH = "users.db"

def init_db():
    """Veritabanı tablosunu oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_new_key(username):
    """Yeni kullanıcı için benzersiz bir API Key üretir."""
    new_key = f"tk_{secrets.token_urlsafe(32)}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, api_key) VALUES (?, ?)", (username, new_key))
        conn.commit()
        return new_key
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def validate_key(api_key):
    """Anahtarın geçerliliğini kontrol eder."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE api_key = ?", (api_key,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# İlk çalıştırmada veritabanını hazırla
if not os.path.exists(DB_PATH):
    init_db()