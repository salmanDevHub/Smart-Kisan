"""
Authentication service — SQLite-backed, no external auth provider needed.

Passwords are hashed with PBKDF2-HMAC-SHA256 (stdlib `hashlib`, no extra
dependency). Sessions use a random opaque token stored in the `sessions`
table (not a JWT) — simple and sufficient for a hackathon-scale app.
"""
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "smart_kisan.db")


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                city TEXT,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()


def signup(name: str, phone: str, password: str, city: str | None) -> dict:
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE phone = ?", (phone,)).fetchone()
        if existing:
            return {"error": "Is phone number se pehle se ek account maujood hai."}
        cur = conn.execute(
            "INSERT INTO users (name, phone, city, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, phone, city, pw_hash, salt, datetime.now(timezone.utc).isoformat()),
        )
        user_id = cur.lastrowid
    return _create_session(user_id, name, phone, city)


def login(phone: str, password: str) -> dict:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        if not row:
            return {"error": "Phone number ya password ghalat hai."}
        pw_hash = _hash_password(password, row["salt"])
        if pw_hash != row["password_hash"]:
            return {"error": "Phone number ya password ghalat hai."}
    return _create_session(row["id"], row["name"], row["phone"], row["city"])


def _create_session(user_id: int, name: str, phone: str, city: str | None) -> dict:
    token = secrets.token_hex(32)
    expires = datetime.now(timezone.utc) + timedelta(days=30)
    with get_db() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires.isoformat()),
        )
    return {"token": token, "user": {"id": user_id, "name": name, "phone": phone, "city": city}}


def get_user_from_token(token: str) -> dict | None:
    with get_db() as conn:
        session = conn.execute(
            "SELECT * FROM sessions WHERE token = ?", (token,)
        ).fetchone()
        if not session:
            return None
        if datetime.fromisoformat(session["expires_at"]) < datetime.now(timezone.utc):
            return None
        user = conn.execute(
            "SELECT id, name, phone, city FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        return dict(user) if user else None
