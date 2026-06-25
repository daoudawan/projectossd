"""
Space Shooter
A Complete Desktop Gaming Application

Created by: Daoud Awaan
Student ID: F2023408101

Features:
  - Login / Register with SQLite
  - Player Profiles & XP System
  - High Scores Leaderboard
  - 10 Progressive Levels
  - Shop System with Upgrades
  - Achievements System
  - Colorful Tkinter Canvas Game

Run:  python main.py
Build EXE:  build.bat
"""

import tkinter as tk
import sys
import os


def resource_path(rel):
    """Support PyInstaller bundled resources."""
    try:
        base = sys._MEIPASS
    except AttributeError:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)


class SpaceShooterApp:
    """Root application — owns the Tk window and screen navigation."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Shooter — by Daoud Awaan F2023408101")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#050510")

        # Try to set window icon (silently skip if missing)
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        from database import Database
        self.db = Database(resource_path("space_shooter.db"))

        self.user_id = None
        self._current_screen = None

        self.show_login()
        self.root.mainloop()

    # ── Screen management ─────────────────────────────────────

    def _clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._current_screen = None

    def set_user(self, user_id):
        self.user_id = user_id

    def show_login(self):
        self._clear()
        self.user_id = None
        from screens import LoginScreen
        self._current_screen = LoginScreen(self.root, self.db, self)

    def show_menu(self):
        self._clear()
        from screens import MainMenuScreen
        self._current_screen = MainMenuScreen(self.root, self.db, self, self.user_id)

    def show_game(self):
        self._clear()
        from screens import GameScreen
        self._current_screen = GameScreen(self.root, self.db, self, self.user_id)

    def show_profile(self):
        self._clear()
        from screens import ProfileScreen
        self._current_screen = ProfileScreen(self.root, self.db, self, self.user_id)

    def show_high_scores(self):
        self._clear()
        from screens import HighScoreScreen
        self._current_screen = HighScoreScreen(self.root, self.db, self, self.user_id)

    def show_shop(self):
        self._clear()
        from screens import ShopScreen
        self._current_screen = ShopScreen(self.root, self.db, self, self.user_id)

    def show_achievements(self):
        self._clear()
        from screens import AchievementsScreen
        self._current_screen = AchievementsScreen(self.root, self.db, self, self.user_id)


def main():
    SpaceShooterApp()


if __name__ == "__main__":
    main()
