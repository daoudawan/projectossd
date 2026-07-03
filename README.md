<div align="center">

# 🚀 Space Shooter

### A Complete Desktop Gaming Application

*An arcade-style space shooter built in pure Python with Tkinter — featuring user accounts, persistent progression, a shop, achievements, and 10 progressive levels.*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](#-license)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Gameplay](#-gameplay)
- [Controls](#-controls)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Building the EXE](#-building-the-exe)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [Shop Items](#-shop-items)
- [Achievements](#-achievements)
- [Levels](#-levels)
- [Author](#-author)
- [License](#-license)

---

## 🌌 Overview

**Space Shooter** is a fully featured desktop game written entirely in Python using the standard `tkinter` Canvas — no external game engine. Players create an account, fight through 10 increasingly difficult levels, earn coins and XP, spend coins in a shop on weapon and defense upgrades, climb a global leaderboard, and unlock achievements. All progress is stored locally in an SQLite database.

> Built as a course project demonstrating GUI programming, object-oriented design, database integration, and application packaging.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Login / Register** | Account system with SQLite-backed, SHA-256 hashed passwords |
| 👤 **Player Profiles** | Track level, XP, coins, high score, games played, total kills |
| 🏆 **High Scores Leaderboard** | Global top-10 plus your personal best runs |
| 🎮 **10 Progressive Levels** | Escalating enemy speed, spawn rate, and boss encounters |
| 🛒 **Shop System** | 10 upgrades — weapons, shields, speed, extra lives, and more |
| 🏅 **Achievements** | 16 unlockable achievements across kills, scores, and milestones |
| 🎨 **Colorful Canvas Game** | Hand-drawn ships, particle explosions, starfield, and coins |
| 💾 **Persistent Progress** | Everything saved locally — pick up where you left off |
| 📦 **Standalone EXE** | One-file Windows executable, no Python install needed |

---

## 🕹️ Gameplay

Pilot your ship through waves of enemies. Each level has a **kill quota** to advance, faster enemies, and tighter spawn timing. Levels **3, 5, 7, 9, and 10** end with a **boss fight**.

- **Enemy types:** Basic, Fast, Tank, and Boss — each with distinct behavior and toughness.
- **Coins** drop from kills — collect them to spend in the shop.
- **XP** accumulates toward your profile level.
- **3 lives** per run, with a brief invincibility window after each hit.

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `←` / `A` | Move left |
| `→` / `D` | Move right |
| `↑` / `W` | Move up |
| `↓` / `S` | Move down |
| `Space` | Shoot |

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **GUI / Rendering:** Tkinter (standard library `Canvas`)
- **Database:** SQLite 3 (`sqlite3`, standard library)
- **Security:** SHA-256 password hashing (`hashlib`)
- **Packaging:** [PyInstaller](https://pyinstaller.org/) (one-file Windows EXE)

> The game runs on the Python standard library alone. The only third-party dependency, **PyInstaller**, is needed solely to build the standalone `.exe`.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or newer** ([download](https://www.python.org/downloads/))
- Tkinter (bundled with standard Python on Windows/macOS)

### Run from source

```bash
# 1. Clone the repository
git clone https://github.com/daoudawan/projectossd.git
cd projectossd

# 2. Run the game
python main.py
```

That's it — no `pip install` required to play. An SQLite database (`space_shooter.db`) is created automatically on first launch.

---

## 📦 Building the EXE

To produce a standalone Windows executable:

```bash
# Install the build tool
pip install -r requirements.txt

# Build (Windows)
build.bat
```

The script runs PyInstaller and outputs **`SpaceShooter_DaoudAwaan.exe`** in the project root (≈12 MB). Double-click to play — no Python required.

Manual equivalent:

```bash
python -m PyInstaller --onefile --windowed --name "SpaceShooter_DaoudAwaan" ^
  --add-data "constants.py;." --add-data "database.py;." ^
  --add-data "game.py;." --add-data "screens.py;." main.py
```

---

## 📁 Project Structure

```
projectossd/
├── main.py            # App entry point — Tk window + screen navigation
├── screens.py         # All UI screens (login, menu, game, shop, etc.)
├── game.py            # Core game engine — ships, bullets, enemies, loop
├── database.py        # SQLite layer — auth, profiles, scores, shop, achievements
├── constants.py       # Colors, fonts, level config, achievement defs
├── build.bat          # One-click PyInstaller build script
├── requirements.txt   # Build dependency (pyinstaller)
└── SpaceShooter_DaoudAwaan.exe   # Prebuilt Windows executable
```

---

## 🏗️ Architecture

The app follows a clean **screen-based navigation** pattern. `SpaceShooterApp` (in [`main.py`](main.py)) owns the root Tk window and swaps screens on demand:

```
SpaceShooterApp (main.py)
   │  owns Tk root + Database
   │
   ├── LoginScreen          → authenticate / register
   ├── MainMenuScreen       → hub navigation
   ├── GameScreen           → hosts the live game (game.py)
   ├── ProfileScreen        → stats & progression
   ├── HighScoreScreen      → leaderboard
   ├── ShopScreen           → buy / view upgrades
   └── AchievementsScreen   → unlocked achievements
```

- **`game.py`** holds the real-time engine: input handling, entity updates, collision, and the render loop on a Tkinter `Canvas`.
- **`database.py`** is the single source of truth for all persistence, exposing a tidy API (`register`, `login`, `save_score`, `buy_item`, `unlock`, …).

---

## 🗄️ Database Schema

SQLite database with six tables:

| Table | Purpose |
|-------|---------|
| `users` | Credentials — username + SHA-256 password hash |
| `profiles` | Per-user level, XP, coins, high score, games played, total kills |
| `high_scores` | Every recorded run (score, level reached, kills, timestamp) |
| `achievements` | Unlocked achievements per user |
| `shop_items` | Catalog of purchasable upgrades (seeded on first run) |
| `inventory` | Items each user owns and their quantities |

---

## 🛒 Shop Items

| Item | Type | Cost | Effect |
|------|------|------|--------|
| Coin Magnet | Boost | 350 | Auto-collect nearby coins |
| XP Booster | Boost | 400 | Earn 2× XP per kill |
| Double Shot | Weapon | 500 | Fire 2 bullets at once |
| Speed Boost | Movement | 600 | Move 50% faster |
| Mega Bomb | Special | 700 | Destroy **all** on-screen enemies |
| Energy Shield | Defense | 800 | Absorbs 3 hits before breaking |
| Extra Life | Life | 1,000 | Gain one extra life |
| Rapid Fire | Weapon | 1,200 | Doubles your fire rate |
| Triple Shot | Weapon | 1,500 | Fire 3 bullets at once |
| Laser Beam | Weapon | 3,000 | Powerful piercing laser shot |

---

## 🏅 Achievements

16 achievements spanning combat, scoring, progression, and economy:

| Achievement | How to unlock |
|-------------|---------------|
| 🩸 First Blood | Kill your first enemy |
| 🔫 Rookie Pilot | Kill 10 enemies in one game |
| ⚔️ Space Warrior | Kill 50 enemies in one game |
| 💥 Destroyer | 100 total kills across all games |
| ☄️ Galaxy Annihilator | 500 total kills across all games |
| 🎯 Point Seeker | Score 1,000 points in one game |
| 📈 High Scorer | Score 10,000 points in one game |
| 👑 Legend | Score 50,000 points in one game |
| 🌟 Rising Star | Reach Level 3 |
| 🦸 Midway Hero | Reach Level 5 |
| 🎖️ Master Pilot | Complete Level 10 |
| 🐉 Boss Slayer | Defeat your first boss |
| 🛍️ Shopaholic | Buy your first shop item |
| 🎮 Regular | Play 5 games |
| 🏆 Veteran | Play 25 games |
| 💰 Galactic Millionaire | Accumulate 5,000 coins |

---

## 📊 Levels

| Level | Kills to clear | Enemy speed | Spawn interval | Boss |
|:-----:|:-------------:|:-----------:|:--------------:|:----:|
| 1 | 8 | 1.5 | 2800 ms | — |
| 2 | 12 | 1.9 | 2400 ms | — |
| 3 | 16 | 2.2 | 2100 ms | ⚠️ |
| 4 | 20 | 2.5 | 1900 ms | — |
| 5 | 25 | 2.8 | 1700 ms | ⚠️ |
| 6 | 30 | 3.1 | 1500 ms | — |
| 7 | 35 | 3.4 | 1300 ms | ⚠️ |
| 8 | 42 | 3.8 | 1100 ms | — |
| 9 | 50 | 4.2 | 950 ms | ⚠️ |
| 10 | 60 | 5.0 | 800 ms | ⚠️ |

---

## 👨‍💻 Author

**Daoud Awan**
🎓 Student ID: `F2023408101`
📧 [f2023408101@umt.edu.pk](mailto:f2023408101@umt.edu.pk)

---

## 📜 License

This project was created for **educational purposes** as a university course project. Feel free to study and learn from the code.

<div align="center">

---

⭐ *If you enjoyed this project, consider giving it a star!* ⭐

**Made with 🐍 Python & ❤️ by Daoud Awan**

</div>
