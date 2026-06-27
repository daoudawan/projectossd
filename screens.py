"""
Space Shooter - UI Screens
Created by: Daoud Awaan (F2023408101)
"""

import tkinter as tk
from tkinter import messagebox
import random
import math
from constants import *
from database import Database
from game import GameEngine


# ─────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────
def make_btn(parent, text, cmd, width=18, color=C_ACCENT, hover=C_ACCENT2,
             bg=C_PANEL, fg_bg=C_BG):
    btn = tk.Button(
        parent, text=text, command=cmd,
        font=F_MED, fg=color, bg=bg,
        activeforeground=hover, activebackground=C_PANEL2,
        relief="flat", bd=0, cursor="hand2",
        highlightbackground=C_BORDER, highlightthickness=1,
        width=width, pady=6
    )
    btn.bind("<Enter>", lambda e: btn.config(fg=hover, bg=C_PANEL2))
    btn.bind("<Leave>", lambda e: btn.config(fg=color, bg=bg))
    return btn


def spacer(parent, h=10):
    tk.Frame(parent, height=h, bg=C_BG).pack(fill="x")


def section_label(parent, text):
    tk.Label(parent, text=text, font=F_LARGE, fg=C_ACCENT, bg=C_BG).pack(pady=(18, 4))
    tk.Frame(parent, height=2, bg=C_BORDER).pack(fill="x", padx=40)


def hud_label(parent, text, fg=C_WHITE):
    return tk.Label(parent, text=text, font=F_SMALL, fg=fg, bg=C_PANEL)


def stars_canvas(parent, w, h, n=60):
    """Return a canvas with a static star field."""
    c = tk.Canvas(parent, width=w, height=h, bg=C_BG, highlightthickness=0)
    for _ in range(n):
        x = random.randint(0, w)
        y = random.randint(0, h)
        r = random.choice([1, 1, 1, 2])
        col = random.choice(STAR_COLORS)
        c.create_oval(x, y, x + r, y + r, fill=col, outline="")
    return c


# ─────────────────────────────────────────────────────────────
# Login Screen
# ─────────────────────────────────────────────────────────────
class LoginScreen(tk.Frame):
    def __init__(self, root, db: Database, app):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self._build()

    def _build(self):
        # Animated stars bg
        self.bg_canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        self._stars = []
        for _ in range(80):
            x = random.randint(0, WIN_W)
            y = random.randint(0, WIN_H)
            r = random.choice([1, 1, 2])
            col = random.choice(STAR_COLORS)
            sid = self.bg_canvas.create_oval(x, y, x+r, y+r, fill=col, outline="")
            spd = random.uniform(0.3, 1.2)
            self._stars.append([sid, x, y, r, spd, col])
        self._animate_stars()

        # Content frame (centered)
        frame = tk.Frame(self, bg=C_PANEL, bd=0,
                         highlightbackground=C_BORDER, highlightthickness=2)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400)

        # Title
        tk.Label(frame, text="🚀 SPACE SHOOTER", font=("Courier New", 22, "bold"),
                 fg=C_ACCENT, bg=C_PANEL).pack(pady=(28, 2))
        tk.Label(frame, text="by Daoud Awaan  F2023408101",
                 font=F_TINY, fg=C_GRAY, bg=C_PANEL).pack(pady=(0, 20))

        # Tabs
        tab_row = tk.Frame(frame, bg=C_PANEL)
        tab_row.pack(fill="x")
        self.mode = tk.StringVar(value="login")
        self._tab_login = tk.Button(tab_row, text="LOGIN", font=F_MED,
                                    fg=C_ACCENT, bg=C_PANEL2, relief="flat",
                                    command=lambda: self._switch("login"), width=10)
        self._tab_register = tk.Button(tab_row, text="REGISTER", font=F_MED,
                                       fg=C_GRAY, bg=C_PANEL, relief="flat",
                                       command=lambda: self._switch("register"), width=10)
        self._tab_login.pack(side="left", fill="x", expand=True)
        self._tab_register.pack(side="left", fill="x", expand=True)

        # Fields
        fld = tk.Frame(frame, bg=C_PANEL)
        fld.pack(padx=30, pady=10, fill="x")

        tk.Label(fld, text="Username", font=F_SMALL, fg=C_GRAY, bg=C_PANEL).pack(anchor="w")
        self.user_var = tk.StringVar()
        self.user_entry = tk.Entry(fld, textvariable=self.user_var,
                                   font=F_MED, bg=C_BG, fg=C_WHITE,
                                   insertbackground=C_ACCENT,
                                   relief="flat", bd=4)
        self.user_entry.pack(fill="x", ipady=4, pady=(2, 10))

        tk.Label(fld, text="Password", font=F_SMALL, fg=C_GRAY, bg=C_PANEL).pack(anchor="w")
        self.pass_var = tk.StringVar()
        self.pass_entry = tk.Entry(fld, textvariable=self.pass_var, show="•",
                                   font=F_MED, bg=C_BG, fg=C_WHITE,
                                   insertbackground=C_ACCENT,
                                   relief="flat", bd=4)
        self.pass_entry.pack(fill="x", ipady=4, pady=(2, 4))

        # Confirm password (register only)
        self.conf_lbl = tk.Label(fld, text="Confirm Password",
                                 font=F_SMALL, fg=C_GRAY, bg=C_PANEL)
        self.conf_var = tk.StringVar()
        self.conf_entry = tk.Entry(fld, textvariable=self.conf_var, show="•",
                                   font=F_MED, bg=C_BG, fg=C_WHITE,
                                   insertbackground=C_ACCENT,
                                   relief="flat", bd=4)

        # Status
        self.status_var = tk.StringVar()
        tk.Label(frame, textvariable=self.status_var,
                 font=F_SMALL, fg=C_RED, bg=C_PANEL,
                 wraplength=340).pack(pady=2)

        # Action button
        self.action_btn = make_btn(frame, "LOGIN", self._action, width=20)
        self.action_btn.pack(pady=(4, 24))

        # Bind Enter key
        frame.bind_all("<Return>", lambda e: self._action())

    def _animate_stars(self):
        if not self.winfo_exists():
            return
        try:
            for s in self._stars:
                sid, x, y, r, spd, col = s
                y += spd
                if y > WIN_H + 4:
                    y = 0
                    x = random.randint(0, WIN_W)
                s[1], s[2] = x, y
                self.bg_canvas.coords(sid, x, y, x + r, y + r)
        except tk.TclError:
            return
        self.after(25, self._animate_stars)

    def _switch(self, mode):
        self.mode.set(mode)
        self.status_var.set("")
        fld = self.pass_entry.master
        if mode == "login":
            self._tab_login.config(fg=C_ACCENT, bg=C_PANEL2)
            self._tab_register.config(fg=C_GRAY, bg=C_PANEL)
            self.conf_lbl.pack_forget()
            self.conf_entry.pack_forget()
            self.action_btn.config(text="LOGIN")
        else:
            self._tab_register.config(fg=C_ACCENT, bg=C_PANEL2)
            self._tab_login.config(fg=C_GRAY, bg=C_PANEL)
            self.conf_lbl.pack(anchor="w")
            self.conf_entry.pack(fill="x", ipady=4, pady=(2, 4))
            self.action_btn.config(text="REGISTER")

    def _action(self):
        username = self.user_var.get().strip()
        password = self.pass_var.get()
        if not username or not password:
            self.status_var.set("Please fill in all fields.")
            return
        if self.mode.get() == "login":
            ok, result = self.db.login(username, password)
            if ok:
                self.app.set_user(result)
                self.app.show_menu()
            else:
                self.status_var.set(result)
        else:
            confirm = self.conf_var.get()
            if password != confirm:
                self.status_var.set("Passwords do not match.")
                return
            ok, result = self.db.register(username, password)
            if ok:
                self.status_var.set("")
                # Auto login
                _, uid = self.db.login(username, password)
                self.app.set_user(uid)
                self.app.show_menu()
            else:
                self.status_var.set(result)


# ─────────────────────────────────────────────────────────────
# Main Menu Screen
# ─────────────────────────────────────────────────────────────
class MainMenuScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self.profile = db.get_profile(user_id)
        self._build()
        self._animate()

    def _build(self):
        # Canvas background
        self.bg = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        self.bg.place(relwidth=1, relheight=1)
        self._stars = []
        for _ in range(100):
            x = random.randint(0, WIN_W)
            y = random.randint(0, WIN_H)
            r = random.choice([1, 1, 1, 2, 2])
            col = random.choice(STAR_COLORS)
            sid = self.bg.create_oval(x, y, x+r, y+r, fill=col, outline="")
            spd = random.uniform(0.3, 1.5)
            self._stars.append([sid, x, y, r, spd])

        # Left panel
        left = tk.Frame(self, bg=C_PANEL, width=260,
                        highlightbackground=C_BORDER, highlightthickness=1)
        left.place(x=0, y=0, width=270, relheight=1)

        # Logo
        tk.Label(left, text="SPACE\nSHOOTER", font=("Courier New", 26, "bold"),
                 fg=C_ACCENT, bg=C_PANEL, justify="center").pack(pady=(40, 2))
        tk.Label(left, text="★ ★ ★", font=("Courier New", 14),
                 fg=C_GOLD, bg=C_PANEL).pack()
        tk.Frame(left, height=2, bg=C_BORDER).pack(fill="x", padx=20, pady=12)

        # Player info
        name = self.profile.get("username", "Pilot") if self.profile else "Pilot"
        coins = self.profile.get("coins", 0) if self.profile else 0
        lvl = self.profile.get("level", 1) if self.profile else 1
        hs = self.profile.get("high_score", 0) if self.profile else 0
        tk.Label(left, text=f"👤  {name}", font=F_MED, fg=C_WHITE, bg=C_PANEL).pack(pady=2)
        tk.Label(left, text=f"💰  {coins:,} coins", font=F_SMALL, fg=C_GOLD, bg=C_PANEL).pack()
        tk.Label(left, text=f"🏆  Best: {hs:,}", font=F_SMALL, fg=C_ORANGE, bg=C_PANEL).pack()
        tk.Frame(left, height=2, bg=C_BORDER).pack(fill="x", padx=20, pady=16)

        # Menu buttons
        buttons = [
            ("▶  PLAY GAME",    self.app.show_game,         C_GREEN),
            ("👤  MY PROFILE",   self.app.show_profile,      C_ACCENT),
            ("🏆  HIGH SCORES",  self.app.show_high_scores,  C_GOLD),
            ("🛒  SHOP",         self.app.show_shop,         C_ORANGE),
            ("🎖  ACHIEVEMENTS", self.app.show_achievements, C_PURPLE),
            ("⬛  LOGOUT",       self.app.show_login,        C_GRAY),
        ]
        for txt, cmd, col in buttons:
            btn = make_btn(left, txt, cmd, width=22, color=col)
            btn.pack(pady=3, padx=16)

        tk.Frame(left, height=10, bg=C_PANEL).pack(expand=True)
        tk.Label(left, text="Made by Daoud Awaan\nF2023408101",
                 font=F_TINY, fg=C_GRAY, bg=C_PANEL, justify="center").pack(pady=12)

        # Right side: animated space scene
        self.right = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        self.right.place(x=270, y=0, relwidth=1, relheight=1, width=-270)

        # Draw decorative ship
        rx, ry = 320, 200
        self.right.create_polygon(
            rx, ry - 60, rx - 30, ry, rx - 50, ry + 40,
            rx - 15, ry + 25, rx, ry + 35, rx + 15, ry + 25,
            rx + 50, ry + 40, rx + 30, ry,
            fill=C_PLAYER, outline=C_PLAYER_GLOW, width=2
        )
        self.right.create_oval(rx - 10, ry - 40, rx + 10, ry - 8,
                               fill="#ccffff", outline="white")

        # Tagline
        self.right.create_text(
            320, 340,
            text="DEFEND THE GALAXY",
            font=("Courier New", 18, "bold"),
            fill=C_ACCENT
        )
        self.right.create_text(
            320, 370,
            text="Survive. Shoot. Conquer.",
            font=("Courier New", 12),
            fill=C_GRAY
        )

    def _animate(self):
        if not self.winfo_exists():
            return
        try:
            for s in self._stars:
                sid, x, y, r, spd = s
                y += spd
                if y > WIN_H + 4:
                    y = 0
                    x = random.randint(0, WIN_W)
                s[1], s[2] = x, y
                self.bg.coords(sid, x, y, x + r, y + r)
        except tk.TclError:
            return
        self.after(20, self._animate)


# ─────────────────────────────────────────────────────────────
# HUD bar above game canvas
# ─────────────────────────────────────────────────────────────
class HUDBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=C_PANEL, height=50)
        self.pack(fill="x")

        self.lv  = tk.Label(self, text="LV 1",  font=F_MED, fg=C_ACCENT,  bg=C_PANEL)
        self.sc  = tk.Label(self, text="Score: 0", font=F_MED, fg=C_GOLD,  bg=C_PANEL)
        self.li  = tk.Label(self, text="❤❤❤",   font=F_MED, fg=C_RED,    bg=C_PANEL)
        self.co  = tk.Label(self, text="💰 0",   font=F_MED, fg=C_GOLD,   bg=C_PANEL)
        self.ki  = tk.Label(self, text="Kills: 0", font=F_SMALL, fg=C_ORANGE, bg=C_PANEL)
        self.sh  = tk.Label(self, text="",        font=F_SMALL, fg=C_SHIELD, bg=C_PANEL)

        self.lv.pack(side="left",  padx=16)
        self.sc.pack(side="left",  padx=12)
        self.li.pack(side="left",  padx=12)
        self.co.pack(side="right", padx=16)
        self.ki.pack(side="right", padx=12)
        self.sh.pack(side="right", padx=8)

    def update(self, level, score, lives, coins, kills, shield):
        self.lv.config(text=f"LV {level}")
        self.sc.config(text=f"Score: {score:,}")
        self.li.config(text="❤" * max(0, lives))
        self.co.config(text=f"💰 {coins:,}")
        self.ki.config(text=f"Kills: {kills}")
        self.sh.config(text=f"🛡 {shield}" if shield > 0 else "")


# ─────────────────────────────────────────────────────────────
# Game Screen
# ─────────────────────────────────────────────────────────────
class GameScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self.profile = db.get_profile(user_id)
        self._build()

    def _build(self):
        self.hud = HUDBar(self)

        self.canvas = tk.Canvas(
            self, width=GAME_W, height=GAME_H,
            bg=C_BG, highlightthickness=0
        )
        self.canvas.pack()

        self.engine = GameEngine(
            self.canvas,
            self.profile,
            on_gameover=self._on_gameover,
            on_level_up=self._on_level_up,
        )

        # Load inventory items for use
        inventory = self.db.get_inventory(self.user_id)
        for item in inventory:
            self.engine.apply_item(item["item_type"], item["id"], item["effect"])

        self.engine.running = True
        self.engine.start(self.canvas, None, None)
        self._hud_loop()

    def _hud_loop(self):
        if not self.engine.running or not self.winfo_exists():
            return
        p = self.engine.player
        if p:
            try:
                self.hud.update(
                    self.engine.level,
                    self.engine.score,
                    p.lives,
                    self.engine.coins_collected,
                    self.engine.total_session_kills,
                    p.shield,
                )
            except tk.TclError:
                return
        self.after(100, self._hud_loop)

    def _on_level_up(self, lvl):
        pass  # HUD updates handle this

    def _on_gameover(self, score, level, kills, coins, victory, boss_killed):
        username = self.profile["username"] if self.profile else "Pilot"

        # Save to DB
        self.db.save_score(self.user_id, username, score, level, kills)
        self.db.add_xp_coins(self.user_id, kills * 5, coins)

        # Check achievements
        self._check_achievements(score, level, kills, boss_killed, victory)

        # Show overlay
        self._show_gameover(score, level, kills, coins, victory)

    def _check_achievements(self, score, level, kills, boss_killed, victory):
        db = self.db
        uid = self.user_id
        prof = db.get_profile(uid)
        total_kills = prof["total_kills"] if prof else kills
        games = prof["games_played"] if prof else 1

        checks = [
            ("first_kill",  kills >= 1,              "First Blood",         "Kill your first enemy"),
            ("kill_10",     kills >= 10,             "Rookie Pilot",        "Kill 10 enemies in one game"),
            ("kill_50",     kills >= 50,             "Space Warrior",       "Kill 50 enemies in one game"),
            ("kill_100_t",  total_kills >= 100,      "Destroyer",           "100 total kills"),
            ("kill_500_t",  total_kills >= 500,      "Galaxy Annihilator",  "500 total kills"),
            ("score_1k",    score >= 1000,           "Point Seeker",        "Score 1,000 points"),
            ("score_10k",   score >= 10000,          "High Scorer",         "Score 10,000 points"),
            ("score_50k",   score >= 50000,          "Legend",              "Score 50,000 points"),
            ("level_3",     level >= 3,              "Rising Star",         "Reach Level 3"),
            ("level_5",     level >= 5,              "Midway Hero",         "Reach Level 5"),
            ("level_10",    victory,                 "Master Pilot",        "Complete Level 10"),
            ("boss_kill",   boss_killed,             "Boss Slayer",         "Defeat your first boss"),
            ("games_5",     games >= 5,              "Regular",             "Play 5 games"),
            ("games_25",    games >= 25,             "Veteran",             "Play 25 games"),
        ]
        if prof and prof.get("coins", 0) >= 5000:
            checks.append(("rich", True, "Galactic Millionaire", "Accumulate 5,000 coins"))

        for key, cond, name, desc in checks:
            if cond:
                db.unlock(uid, key, name, desc)

    def _show_gameover(self, score, level, kills, coins, victory):
        overlay = tk.Toplevel(self.winfo_toplevel())
        overlay.title("Game Over")
        overlay.geometry("460x500")
        overlay.configure(bg=C_PANEL)
        overlay.resizable(False, False)
        overlay.grab_set()
        overlay.transient(self.winfo_toplevel())

        title = "🏆 VICTORY!" if victory else "💀 GAME OVER"
        color = C_GOLD if victory else C_RED
        tk.Label(overlay, text=title, font=("Courier New", 26, "bold"),
                 fg=color, bg=C_PANEL).pack(pady=(30, 8))

        tk.Frame(overlay, height=2, bg=C_BORDER).pack(fill="x", padx=30, pady=4)

        stats = [
            ("Score",         f"{score:,}",  C_GOLD),
            ("Level Reached", str(level),    C_ACCENT),
            ("Enemies Killed",str(kills),    C_ORANGE),
            ("Coins Earned",  f"{coins:,}",  C_GOLD),
        ]
        for lbl, val, col in stats:
            row = tk.Frame(overlay, bg=C_PANEL)
            row.pack(fill="x", padx=50, pady=3)
            tk.Label(row, text=lbl, font=F_SMALL, fg=C_GRAY, bg=C_PANEL, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=F_MED,   fg=col,   bg=C_PANEL, anchor="e").pack(side="right")

        tk.Frame(overlay, height=2, bg=C_BORDER).pack(fill="x", padx=30, pady=12)

        def go_menu():
            overlay.destroy()
            self.app.show_menu()

        def play_again():
            overlay.destroy()
            self.app.show_game()

        make_btn(overlay, "▶ PLAY AGAIN", play_again, width=20, color=C_GREEN).pack(pady=6)
        make_btn(overlay, "◀ MAIN MENU", go_menu, width=20, color=C_ACCENT).pack(pady=6)


# ─────────────────────────────────────────────────────────────
# Profile Screen
# ─────────────────────────────────────────────────────────────
class ProfileScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self._build()

    def _build(self):
        section_label(self, "👤  MY PROFILE")

        profile = self.db.get_profile(self.user_id)
        if not profile:
            tk.Label(self, text="Profile not found.", fg=C_RED, bg=C_BG).pack()
            return

        # Stats panel
        panel = tk.Frame(self, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
        panel.pack(padx=60, pady=16, fill="x")

        stats = [
            ("Username",      profile.get("username", "—"),                          C_ACCENT),
            ("Player Level",  str(profile.get("level", 1)),                          C_ORANGE),
            ("Experience",    f"{profile.get('xp', 0):,} XP",                        C_GREEN),
            ("Coins",         f"{profile.get('coins', 0):,} 💰",                      C_GOLD),
            ("High Score",    f"{profile.get('high_score', 0):,}",                   C_GOLD),
            ("Games Played",  str(profile.get("games_played", 0)),                   C_WHITE),
            ("Total Kills",   f"{profile.get('total_kills', 0):,}",                  C_ORANGE),
        ]
        for lbl, val, col in stats:
            row = tk.Frame(panel, bg=C_PANEL)
            row.pack(fill="x", padx=30, pady=5)
            tk.Label(row, text=lbl, font=F_SMALL, fg=C_GRAY, bg=C_PANEL, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=F_MED,   fg=col,   bg=C_PANEL, anchor="e").pack(side="right")

        # Recent scores
        section_label(self, "Recent Scores")
        scores = self.db.player_scores(self.user_id, 5)
        if scores:
            tbl = tk.Frame(self, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
            tbl.pack(padx=60, pady=4, fill="x")
            hrow = tk.Frame(tbl, bg=C_PANEL2)
            hrow.pack(fill="x")
            for h, w in [("Score", 12), ("Level", 8), ("Kills", 8), ("Date", 22)]:
                tk.Label(hrow, text=h, font=F_SMALL, fg=C_ACCENT, bg=C_PANEL2,
                         width=w, anchor="center").pack(side="left")
            for s in scores:
                row = tk.Frame(tbl, bg=C_PANEL)
                row.pack(fill="x")
                date = s.get("played_at", "")[:10]
                for val, w in [(f"{s['score']:,}", 12), (str(s['level_reached']), 8),
                               (str(s['kills']), 8), (date, 22)]:
                    tk.Label(row, text=val, font=F_SMALL, fg=C_WHITE, bg=C_PANEL,
                             width=w, anchor="center").pack(side="left")
        else:
            tk.Label(self, text="No scores yet. Play your first game!",
                     fg=C_GRAY, font=F_SMALL, bg=C_BG).pack(pady=6)

        spacer(self, 16)
        make_btn(self, "◀ BACK TO MENU", self.app.show_menu, width=20).pack()


# ─────────────────────────────────────────────────────────────
# High Scores Screen
# ─────────────────────────────────────────────────────────────
class HighScoreScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self._build()

    def _build(self):
        section_label(self, "🏆  GLOBAL HIGH SCORES")

        scores = self.db.top_scores(10)

        outer = tk.Frame(self, bg=C_PANEL, highlightbackground=C_BORDER, highlightthickness=1)
        outer.pack(padx=50, pady=12, fill="x")

        # Header
        hrow = tk.Frame(outer, bg=C_PANEL2)
        hrow.pack(fill="x")
        hdrs = [("#", 4), ("Player", 14), ("Score", 12), ("Level", 8), ("Kills", 8), ("Date", 14)]
        for h, w in hdrs:
            tk.Label(hrow, text=h, font=F_SMALL, fg=C_ACCENT, bg=C_PANEL2,
                     width=w, anchor="center", pady=6).pack(side="left")

        medal = ["🥇", "🥈", "🥉"]
        for i, s in enumerate(scores):
            bg = C_PANEL2 if i % 2 == 0 else C_PANEL
            row = tk.Frame(outer, bg=bg)
            row.pack(fill="x")
            rank = medal[i] if i < 3 else str(i + 1)
            date = s.get("played_at", "")[:10]
            score_col = C_GOLD if i == 0 else (C_GRAY if i > 4 else C_WHITE)
            vals = [(rank, 4), (s["username"], 14), (f"{s['score']:,}", 12),
                    (str(s["level_reached"]), 8), (str(s["kills"]), 8), (date, 14)]
            for val, w in vals:
                tk.Label(row, text=val, font=F_SMALL, fg=score_col, bg=bg,
                         width=w, anchor="center", pady=5).pack(side="left")

        if not scores:
            tk.Label(outer, text="No scores yet! Be the first to play.",
                     fg=C_GRAY, font=F_SMALL, bg=C_PANEL, pady=20).pack()

        spacer(self, 20)
        make_btn(self, "◀ BACK TO MENU", self.app.show_menu, width=20).pack()


# ─────────────────────────────────────────────────────────────
# Shop Screen
# ─────────────────────────────────────────────────────────────
class ShopScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self._build()

    def _build(self):
        section_label(self, "🛒  SPACE SHOP")

        profile = self.db.get_profile(self.user_id)
        self.coins_var = tk.StringVar(value=f"💰  {profile.get('coins', 0):,} coins" if profile else "0")

        tk.Label(self, textvariable=self.coins_var, font=F_LARGE,
                 fg=C_GOLD, bg=C_BG).pack(pady=4)

        # Status message
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, font=F_SMALL,
                 fg=C_GREEN, bg=C_BG).pack()

        # Scrollable item grid
        container = tk.Frame(self, bg=C_BG)
        container.pack(fill="both", expand=True, padx=30, pady=8)

        canvas = tk.Canvas(container, bg=C_BG, highlightthickness=0)
        scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=C_BG)

        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        items = self.db.get_shop_items()
        inventory = {i["id"]: i["quantity"] for i in self.db.get_inventory(self.user_id)}

        type_colors = {
            "weapon":   C_RED,
            "defense":  C_SHIELD,
            "movement": C_GREEN,
            "life":     C_PINK,
            "special":  C_PURPLE,
            "boost":    C_ORANGE,
        }
        type_icons = {
            "weapon": "⚔", "defense": "🛡", "movement": "⚡",
            "life": "❤", "special": "💥", "boost": "⬆",
        }

        cols = 2
        for idx, item in enumerate(items):
            row_n, col_n = divmod(idx, cols)
            cell = tk.Frame(inner, bg=C_PANEL,
                            highlightbackground=C_BORDER, highlightthickness=1)
            cell.grid(row=row_n, column=col_n, padx=8, pady=8, sticky="nsew", ipadx=8, ipady=8)
            inner.columnconfigure(col_n, weight=1)

            itype = item["item_type"]
            col = type_colors.get(itype, C_WHITE)
            icon = type_icons.get(itype, "•")

            tk.Label(cell, text=f"{icon}  {item['name']}", font=F_MED,
                     fg=col, bg=C_PANEL).pack(anchor="w")
            tk.Label(cell, text=item["description"], font=F_TINY,
                     fg=C_GRAY, bg=C_PANEL, wraplength=170, justify="left").pack(anchor="w")

            bottom = tk.Frame(cell, bg=C_PANEL)
            bottom.pack(fill="x", pady=(6, 0))
            tk.Label(bottom, text=f"💰 {item['cost']:,}", font=F_SMALL,
                     fg=C_GOLD, bg=C_PANEL).pack(side="left")

            qty = inventory.get(item["id"], 0)
            if qty:
                tk.Label(bottom, text=f"Owned: {qty}", font=F_TINY,
                         fg=C_GREEN, bg=C_PANEL).pack(side="left", padx=6)

            iid = item["id"]
            btn = tk.Button(bottom, text="BUY", font=F_SMALL,
                            fg=C_BG, bg=col, activebackground=C_BORDER,
                            relief="flat", cursor="hand2", padx=8,
                            command=lambda i=iid, n=item["name"], c=item["cost"]: self._buy(i, n, c))
            btn.pack(side="right")

        spacer(self, 12)
        make_btn(self, "◀ BACK TO MENU", self.app.show_menu, width=20).pack()

    def _buy(self, item_id, name, cost):
        ok, msg = self.db.buy_item(self.user_id, item_id)
        if ok:
            # Check first purchase achievement
            self.db.unlock(self.user_id, "first_buy", "Shopaholic", "Buy your first shop item")
            self.status_var.set(f"✓ {msg}")
            profile = self.db.get_profile(self.user_id)
            self.coins_var.set(f"💰  {profile.get('coins', 0):,} coins")
        else:
            self.status_var.set(f"✗ {msg}")


# ─────────────────────────────────────────────────────────────
# Achievements Screen
# ─────────────────────────────────────────────────────────────
class AchievementsScreen(tk.Frame):
    def __init__(self, root, db: Database, app, user_id):
        super().__init__(root, bg=C_BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.app = app
        self.user_id = user_id
        self._build()

    def _build(self):
        section_label(self, "🎖  ACHIEVEMENTS")

        unlocked_set = {a["key"] for a in self.db.get_achievements(self.user_id)}

        tk.Label(self,
                 text=f"Unlocked: {len(unlocked_set)} / {len(ACHIEVEMENTS)}",
                 font=F_MED, fg=C_ACCENT, bg=C_BG).pack(pady=4)

        # Scrollable list
        container = tk.Frame(self, bg=C_BG)
        container.pack(fill="both", expand=True, padx=30, pady=8)

        canvas = tk.Canvas(container, bg=C_BG, highlightthickness=0)
        scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=C_BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        cols = 2
        for idx, (key, name, desc) in enumerate(ACHIEVEMENTS):
            row_n, col_n = divmod(idx, cols)
            done = key in unlocked_set
            bg = C_PANEL2 if done else C_PANEL
            border = C_GOLD if done else C_BORDER

            cell = tk.Frame(inner, bg=bg,
                            highlightbackground=border, highlightthickness=1)
            cell.grid(row=row_n, column=col_n, padx=8, pady=6, sticky="nsew",
                      ipadx=10, ipady=8)
            inner.columnconfigure(col_n, weight=1)

            status = "✅" if done else "🔒"
            name_col = C_GOLD if done else C_GRAY

            tk.Label(cell, text=f"{status}  {name}", font=F_MED,
                     fg=name_col, bg=bg, anchor="w").pack(fill="x")
            tk.Label(cell, text=desc, font=F_TINY,
                     fg=C_GRAY if not done else C_WHITE, bg=bg,
                     wraplength=200, justify="left", anchor="w").pack(fill="x")

        spacer(self, 12)
        make_btn(self, "◀ BACK TO MENU", self.app.show_menu, width=20).pack()
