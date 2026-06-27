"""
Space Shooter - Database Module
Created by: Daoud Awaan (F2023408101)
"""

import sqlite3
import hashlib
from datetime import datetime


class Database:
    def __init__(self, path="space_shooter.db"):
        self.path = path
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self._conn() as conn:
            c = conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                high_score INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                total_kills INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                score INTEGER,
                level_reached INTEGER,
                kills INTEGER,
                played_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                key TEXT,
                name TEXT,
                description TEXT,
                unlocked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, key),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS shop_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                item_type TEXT,
                cost INTEGER,
                effect REAL
            )""")

            c.execute("""CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_id INTEGER,
                quantity INTEGER DEFAULT 1,
                UNIQUE(user_id, item_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(item_id) REFERENCES shop_items(id)
            )""")

            # Seed shop items
            if c.execute("SELECT COUNT(*) FROM shop_items").fetchone()[0] == 0:
                items = [
                    ("Double Shot",   "Fire 2 bullets simultaneously",   "weapon",   500,  2.0),
                    ("Triple Shot",   "Fire 3 bullets simultaneously",   "weapon",  1500,  3.0),
                    ("Laser Beam",    "Powerful piercing laser shot",    "weapon",  3000,  5.0),
                    ("Rapid Fire",    "Doubles your fire rate",          "weapon",  1200,  2.0),
                    ("Energy Shield", "Absorbs 3 hits before breaking",  "defense",  800,  3.0),
                    ("Speed Boost",   "Move 50% faster",                "movement", 600,  1.5),
                    ("Extra Life",    "Gain one extra life",             "life",    1000,  1.0),
                    ("Mega Bomb",     "Destroy ALL enemies on screen",   "special",  700,  1.0),
                    ("XP Booster",   "Earn 2x XP per kill",            "boost",    400,  2.0),
                    ("Coin Magnet",   "Auto-collect nearby coins",       "boost",    350,  1.0),
                ]
                c.executemany(
                    "INSERT INTO shop_items(name,description,item_type,cost,effect) VALUES(?,?,?,?,?)",
                    items
                )
            conn.commit()

    # ---------- Auth ----------

    @staticmethod
    def _hash(pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    def register(self, username, password):
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        if len(password) < 4:
            return False, "Password must be at least 4 characters."
        try:
            with self._conn() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO users(username, password_hash) VALUES(?,?)",
                          (username.strip(), self._hash(password)))
                uid = c.lastrowid
                c.execute("INSERT INTO profiles(user_id) VALUES(?)", (uid,))
                conn.commit()
            return True, uid
        except sqlite3.IntegrityError:
            return False, "Username already taken."

    def login(self, username, password):
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE username=? AND password_hash=?",
                (username.strip(), self._hash(password))
            ).fetchone()
        if row:
            return True, row["id"]
        return False, "Invalid username or password."

    # ---------- Profile ----------

    def get_profile(self, user_id):
        with self._conn() as conn:
            row = conn.execute(
                """SELECT u.username, p.* FROM users u
                   JOIN profiles p ON u.id=p.user_id
                   WHERE u.id=?""", (user_id,)
            ).fetchone()
        return dict(row) if row else None

    def add_xp_coins(self, user_id, xp, coins):
        with self._conn() as conn:
            conn.execute(
                "UPDATE profiles SET xp=xp+?, coins=coins+? WHERE user_id=?",
                (xp, coins, user_id)
            )

    def spend_coins(self, user_id, amount):
        with self._conn() as conn:
            row = conn.execute("SELECT coins FROM profiles WHERE user_id=?", (user_id,)).fetchone()
            if not row or row["coins"] < amount:
                return False
            conn.execute("UPDATE profiles SET coins=coins-? WHERE user_id=?", (amount, user_id))
        return True

    # ---------- Scores ----------

    def save_score(self, user_id, username, score, level_reached, kills):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO high_scores(user_id,username,score,level_reached,kills) VALUES(?,?,?,?,?)",
                (user_id, username, score, level_reached, kills)
            )
            conn.execute(
                """UPDATE profiles SET
                   high_score=MAX(high_score,?),
                   games_played=games_played+1,
                   total_kills=total_kills+?
                   WHERE user_id=?""",
                (score, kills, user_id)
            )

    def top_scores(self, limit=10):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT username,score,level_reached,kills,played_at FROM high_scores ORDER BY score DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def player_scores(self, user_id, limit=5):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT score,level_reached,kills,played_at FROM high_scores WHERE user_id=? ORDER BY score DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
        return [dict(r) for r in rows]

    # ---------- Shop ----------

    def get_shop_items(self):
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM shop_items ORDER BY cost").fetchall()
        return [dict(r) for r in rows]

    def get_inventory(self, user_id):
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT s.*, i.quantity FROM shop_items s
                   JOIN inventory i ON s.id=i.item_id
                   WHERE i.user_id=?""", (user_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    def buy_item(self, user_id, item_id):
        with self._conn() as conn:
            item = conn.execute("SELECT * FROM shop_items WHERE id=?", (item_id,)).fetchone()
            if not item:
                return False, "Item not found."
            profile = conn.execute("SELECT coins FROM profiles WHERE user_id=?", (user_id,)).fetchone()
            if not profile or profile["coins"] < item["cost"]:
                return False, f"Need {item['cost']} coins."
            conn.execute("UPDATE profiles SET coins=coins-? WHERE user_id=?", (item["cost"], user_id))
            conn.execute(
                """INSERT INTO inventory(user_id,item_id,quantity) VALUES(?,?,1)
                   ON CONFLICT(user_id,item_id) DO UPDATE SET quantity=quantity+1""",
                (user_id, item_id)
            )
        return True, f"Purchased {item['name']}!"

    def use_item(self, user_id, item_id):
        with self._conn() as conn:
            row = conn.execute(
                "SELECT quantity FROM inventory WHERE user_id=? AND item_id=?", (user_id, item_id)
            ).fetchone()
            if not row or row["quantity"] < 1:
                return False
            if row["quantity"] == 1:
                conn.execute("DELETE FROM inventory WHERE user_id=? AND item_id=?", (user_id, item_id))
            else:
                conn.execute(
                    "UPDATE inventory SET quantity=quantity-1 WHERE user_id=? AND item_id=?",
                    (user_id, item_id)
                )
        return True

    # ---------- Achievements ----------

    def unlock(self, user_id, key, name, description):
        try:
            with self._conn() as conn:
                conn.execute(
                    "INSERT INTO achievements(user_id,key,name,description) VALUES(?,?,?,?)",
                    (user_id, key, name, description)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def has_achievement(self, user_id, key):
        with self._conn() as conn:
            return conn.execute(
                "SELECT 1 FROM achievements WHERE user_id=? AND key=?", (user_id, key)
            ).fetchone() is not None

    def get_achievements(self, user_id):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM achievements WHERE user_id=? ORDER BY unlocked_at DESC",
                (user_id,)
            ).fetchall()
        return [dict(r) for r in rows]
