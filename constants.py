"""
Space Shooter - Constants
Created by: Daoud Awaan (F2023408101)
"""

# Window
WIN_W = 900
WIN_H = 700
GAME_W = 900
GAME_H = 600

# ── Colors ──────────────────────────────────────────────────
C_BG        = "#050510"
C_PANEL     = "#0a0a28"
C_PANEL2    = "#0d1240"
C_BORDER    = "#1a1a5a"
C_ACCENT    = "#00ffff"
C_ACCENT2   = "#0066ff"
C_GOLD      = "#ffd700"
C_GREEN     = "#00ff88"
C_RED       = "#ff3344"
C_ORANGE    = "#ff8800"
C_PURPLE    = "#bb00ff"
C_PINK      = "#ff0080"
C_WHITE     = "#ffffff"
C_GRAY      = "#556677"
C_DARK_GRAY = "#223"

# Star colors
STAR_COLORS = ["#ffffff", "#aabbff", "#ffff99", "#ffccdd", "#ccffff", "#ffddaa"]

# Ships
C_PLAYER       = "#00ddff"
C_PLAYER_GLOW  = "#0044ff"
C_PLAYER_ENG   = "#ff6600"
C_ENEMY_BASIC  = "#ff2222"
C_ENEMY_FAST   = "#ff8800"
C_ENEMY_TANK   = "#bb00ff"
C_ENEMY_BOSS   = "#ff0055"
C_BULLET_P     = "#ffff00"
C_BULLET_E     = "#ff5555"
C_COIN         = "#ffd700"
C_SHIELD       = "#00ffff"
C_EXPLOSION    = ["#ffff00", "#ff8800", "#ff4400", "#ff0000", "#ff00aa"]

# ── Fonts ────────────────────────────────────────────────────
F_TITLE  = ("Courier New", 30, "bold")
F_LARGE  = ("Courier New", 17, "bold")
F_MED    = ("Courier New", 13, "bold")
F_SMALL  = ("Courier New", 11)
F_TINY   = ("Courier New", 9)

# ── Gameplay ─────────────────────────────────────────────────
PLAYER_SPEED   = 6
PLAYER_LIVES   = 3
SHOOT_DELAY    = 260      # ms between shots
BULLET_SPEED   = 11
E_BULLET_SPEED = 4
COIN_SPEED     = 2.5
STAR_COUNT     = 120
INVINCIBLE_MS  = 2500     # ms player is invincible after hit

# Level config dict: kills_needed, enemy_base_speed, spawn_ms, has_boss
LEVELS = {
    1:  (8,   1.5, 2800, False),
    2:  (12,  1.9, 2400, False),
    3:  (16,  2.2, 2100, True),
    4:  (20,  2.5, 1900, False),
    5:  (25,  2.8, 1700, True),
    6:  (30,  3.1, 1500, False),
    7:  (35,  3.4, 1300, True),
    8:  (42,  3.8, 1100, False),
    9:  (50,  4.2,  950, True),
    10: (60,  5.0,  800, True),
}
MAX_LEVEL = 10

# ── Achievements ─────────────────────────────────────────────
ACHIEVEMENTS = [
    ("first_kill",  "First Blood",         "Kill your first enemy"),
    ("kill_10",     "Rookie Pilot",         "Kill 10 enemies in one game"),
    ("kill_50",     "Space Warrior",        "Kill 50 enemies in one game"),
    ("kill_100_t",  "Destroyer",            "100 total kills across all games"),
    ("kill_500_t",  "Galaxy Annihilator",   "500 total kills across all games"),
    ("score_1k",    "Point Seeker",         "Score 1,000 points in one game"),
    ("score_10k",   "High Scorer",          "Score 10,000 points in one game"),
    ("score_50k",   "Legend",               "Score 50,000 points in one game"),
    ("level_3",     "Rising Star",          "Reach Level 3"),
    ("level_5",     "Midway Hero",          "Reach Level 5"),
    ("level_10",    "Master Pilot",         "Complete Level 10"),
    ("boss_kill",   "Boss Slayer",          "Defeat your first boss"),
    ("first_buy",   "Shopaholic",           "Buy your first shop item"),
    ("games_5",     "Regular",              "Play 5 games"),
    ("games_25",    "Veteran",              "Play 25 games"),
    ("rich",        "Galactic Millionaire", "Accumulate 5,000 coins"),
]
