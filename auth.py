import hashlib
SALT = b'pfm_salt_v1'

class Auth:
    def __init__(self, db):
        self.db = db

    def _hash_password(self, password: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100_000).hex()

    def register(self, username: str, password: str) -> bool:
        try:
            hashed = self._hash_password(password)
            cur = self.db.conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            self.db.conn.commit()
            print("✅ Registration successful.")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def login(self, username: str, password: str):
        hashed = self._hash_password(password)
        cur = self.db.conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed))
        row = cur.fetchone()
        if row:
            print("✅ Login successful.")
            return row["id"]
        else:
            print("❌ Invalid credentials.")
            return None
