"""
Space Shooter - Game Engine
Created by: Daoud Awaan (F2023408101)
"""

import tkinter as tk
import random
import math
from constants import *


# ─────────────────────────────────────────────────────────────
# Star Background
# ─────────────────────────────────────────────────────────────
class Star:
    def __init__(self, canvas):
        self.canvas = canvas
        self.reset(random.randint(0, GAME_H))

    def reset(self, y=0):
        self.x = random.uniform(0, GAME_W)
        self.y = y
        self.size = random.choice([5, 5, 5, 10, 10, 15])
        self.speed = random.uniform(0.4, 2.2)
        self.color = random.choice(STAR_COLORS)
        self.alpha_step = random.choice([0, 0, 1])  # occasional twinkle
        self.id = self.canvas.create_oval(
            self.x, self.y, self.x + self.size, self.y + self.size,
            fill=self.color, outline=""
        )

    def update(self):
        self.y += self.speed
        self.canvas.coords(self.id,
                           self.x, self.y,
                           self.x + self.size, self.y + self.size)
        if self.y > GAME_H + 5:
            self.canvas.delete(self.id)
            self.reset()


# ─────────────────────────────────────────────────────────────
# Explosion Effect
# ─────────────────────────────────────────────────────────────
class Explosion:
    def __init__(self, canvas, x, y, size=1.0):
        self.canvas = canvas
        self.x, self.y = x, y
        self.particles = []
        n = int(12 * size)
        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 5.0) * size
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            r = random.randint(2, int(6 * size))
            color = random.choice(C_EXPLOSION)
            pid = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="")
            self.particles.append([pid, x, y, dx, dy, r, 0, color])
        self.alive = True
        self.life = 0

    def update(self):
        self.life += 1
        done = True
        for p in self.particles:
            pid, x, y, dx, dy, r, age, color = p
            if pid is None:
                continue
            done = False
            nx, ny = x + dx, y + dy
            p[1], p[2] = nx, ny
            p[4] = dy + 0.15  # gravity
            p[6] += 1
            fade = max(2, r - p[6] // 3)
            self.canvas.coords(pid, nx - fade, ny - fade, nx + fade, ny + fade)
            if p[6] > 15 or fade < 1:
                self.canvas.delete(pid)
                p[0] = None
        if done or self.life > 25:
            self.alive = False


# ─────────────────────────────────────────────────────────────
# Floating Score Text
# ─────────────────────────────────────────────────────────────
class FloatText:
    def __init__(self, canvas, x, y, text, color=C_GOLD):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.life = 0
        self.id = canvas.create_text(x, y, text=text, fill=color,
                                     font=F_SMALL, anchor="center")

    def update(self):
        self.life += 1
        self.y -= 1
        self.canvas.coords(self.id, self.x, self.y)
        if self.life > 35:
            self.canvas.delete(self.id)
            return False
        return True


# ─────────────────────────────────────────────────────────────
# Coin
# ─────────────────────────────────────────────────────────────
class Coin:
    def __init__(self, canvas, x, y, value=10):
        self.canvas = canvas
        self.x, self.y = x, y
        self.value = value
        self.speed = COIN_SPEED
        self.alive = True
        r = 7
        self.body = canvas.create_oval(x - r, y - r, x + r, y + r,
                                       fill=C_COIN, outline="#ffaa00", width=2)
        self.label = canvas.create_text(x, y, text="$", fill="#8b6914",
                                        font=("Courier New", 7, "bold"))

    def update(self):
        self.y += self.speed
        self.canvas.move(self.body, 0, self.speed)
        self.canvas.move(self.label, 0, self.speed)
        if self.y > GAME_H + 20:
            self.destroy()

    def destroy(self):
        self.alive = False
        self.canvas.delete(self.body)
        self.canvas.delete(self.label)

    def rect(self):
        return (self.x - 7, self.y - 7, self.x + 7, self.y + 7)


# ─────────────────────────────────────────────────────────────
# Bullet
# ─────────────────────────────────────────────────────────────
class Bullet:
    def __init__(self, canvas, x, y, dy, is_enemy=False, spread=0):
        self.canvas = canvas
        self.x = x + spread
        self.y = y
        self.dy = dy
        self.is_enemy = is_enemy
        self.alive = True
        if is_enemy:
            self.ids = [canvas.create_oval(self.x - 3, y - 3, self.x + 3, y + 3,
                                           fill=C_BULLET_E, outline="#ff8888")]
        else:
            self.ids = [
                canvas.create_rectangle(self.x - 2, y - 14, self.x + 2, y,
                                        fill=C_BULLET_P, outline=""),
                canvas.create_oval(self.x - 3, y - 16, self.x + 3, y - 10,
                                   fill="#ffffff", outline=""),
            ]

    def update(self):
        self.y += self.dy
        for i in self.ids:
            self.canvas.move(i, 0, self.dy)
        if self.y < -20 or self.y > GAME_H + 20:
            self.destroy()

    def destroy(self):
        self.alive = False
        for i in self.ids:
            self.canvas.delete(i)

    def rect(self):
        return (self.x - 3, self.y - 16, self.x + 3, self.y)


# ─────────────────────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────────────────────
class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = GAME_W // 2
        self.y = GAME_H - 60
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.shield = 0
        self.rapid_fire = False
        self.shoot_mode = "single"  # single | double | triple | laser
        self.invincible = False
        self.inv_until = 0
        self.blink_on = True
        self.alive = True
        self.parts = []
        self._draw()

    def _draw(self):
        for p in self.parts:
            self.canvas.delete(p)
        self.parts = []
        if not self.blink_on:
            return
        x, y = self.x, self.y
        # Main fuselage
        self.parts.append(self.canvas.create_polygon(
            x,      y - 28,
            x - 8,  y - 10,
            x - 18, y + 12,
            x - 6,  y + 6,
            x,      y + 14,
            x + 6,  y + 6,
            x + 18, y + 12,
            x + 8,  y - 10,
            fill=C_PLAYER, outline=C_PLAYER_GLOW, width=2
        ))
        # Cockpit
        self.parts.append(self.canvas.create_oval(
            x - 6, y - 20, x + 6, y - 4,
            fill="#ccffff", outline="#ffffff", width=1
        ))
        # Left engine
        self.parts.append(self.canvas.create_oval(
            x - 18, y + 10, x - 10, y + 18,
            fill=C_PLAYER_ENG, outline="#ffcc00", width=1
        ))
        # Right engine
        self.parts.append(self.canvas.create_oval(
            x + 10, y + 10, x + 18, y + 18,
            fill=C_PLAYER_ENG, outline="#ffcc00", width=1
        ))
        # Engine flame (animated feel)
        self.parts.append(self.canvas.create_polygon(
            x - 16, y + 18, x - 12, y + 28, x - 8,  y + 18,
            fill="#ff4400", outline=""
        ))
        self.parts.append(self.canvas.create_polygon(
            x + 8,  y + 18, x + 12, y + 28, x + 16, y + 18,
            fill="#ff4400", outline=""
        ))
        # Shield ring
        if self.shield > 0:
            self.parts.append(self.canvas.create_oval(
                x - 26, y - 28, x + 26, y + 20,
                outline=C_SHIELD, width=2, dash=(4, 4)
            ))

    def move(self, dx, dy):
        self.x = max(22, min(GAME_W - 22, self.x + dx * self.speed))
        self.y = max(30, min(GAME_H - 20, self.y + dy * self.speed))

    def take_hit(self):
        if self.invincible:
            return False
        if self.shield > 0:
            self.shield -= 1
            return False
        self.lives -= 1
        if self.lives > 0:
            self.invincible = True
            import time
            self.inv_until = time.time() * 1000 + INVINCIBLE_MS
        return self.lives <= 0

    def update(self):
        import time
        if self.invincible:
            now = time.time() * 1000
            if now >= self.inv_until:
                self.invincible = False
                self.blink_on = True
            else:
                self.blink_on = not self.blink_on
        self._draw()

    def destroy(self):
        for p in self.parts:
            self.canvas.delete(p)
        self.parts = []

    def rect(self):
        return (self.x - 16, self.y - 26, self.x + 16, self.y + 14)


# ─────────────────────────────────────────────────────────────
# Enemies
# ─────────────────────────────────────────────────────────────
class Enemy:
    KIND_BASIC = "basic"
    KIND_FAST  = "fast"
    KIND_TANK  = "tank"

    def __init__(self, canvas, x, y, kind=KIND_BASIC, speed=2.0):
        self.canvas = canvas
        self.x, self.y = x, y
        self.kind = kind
        self.speed = speed
        self.alive = True
        self.parts = []
        self.shoot_timer = random.randint(60, 180)
        self.wobble = random.uniform(-0.5, 0.5)
        self.wobble_tick = 0

        if kind == self.KIND_BASIC:
            self.max_hp = 1
            self.score = 100
            self.coins = random.randint(5, 15)
            self.xp = 10
        elif kind == self.KIND_FAST:
            self.max_hp = 1
            self.score = 150
            self.coins = random.randint(8, 20)
            self.xp = 15
            self.speed *= 1.6
        else:  # tank
            self.max_hp = 3
            self.score = 300
            self.coins = random.randint(20, 40)
            self.xp = 30
            self.speed *= 0.7

        self.hp = self.max_hp
        self._draw()

    def _draw(self):
        for p in self.parts:
            self.canvas.delete(p)
        self.parts = []
        x, y = self.x, self.y
        k = self.kind
        hp_ratio = self.hp / self.max_hp

        if k == self.KIND_BASIC:
            c = C_ENEMY_BASIC
            # Inverted V shape
            self.parts.append(self.canvas.create_polygon(
                x,      y + 20,
                x - 18, y - 8,
                x - 8,  y - 4,
                x,      y - 14,
                x + 8,  y - 4,
                x + 18, y - 8,
                fill=c, outline="#ff8888", width=1
            ))
            self.parts.append(self.canvas.create_oval(
                x - 5, y + 2, x + 5, y + 12,
                fill="#ff8888", outline=""
            ))

        elif k == self.KIND_FAST:
            c = C_ENEMY_FAST
            # Thin dart
            self.parts.append(self.canvas.create_polygon(
                x,      y + 22,
                x - 12, y,
                x - 5,  y - 2,
                x,      y - 16,
                x + 5,  y - 2,
                x + 12, y,
                fill=c, outline="#ffcc66", width=1
            ))
            self.parts.append(self.canvas.create_oval(
                x - 4, y - 4, x + 4, y + 6,
                fill="#ffffff", outline=""
            ))

        else:  # tank
            c = C_ENEMY_TANK
            # Wide hexagon
            self.parts.append(self.canvas.create_polygon(
                x,      y + 26,
                x - 22, y + 10,
                x - 22, y - 10,
                x,      y - 22,
                x + 22, y - 10,
                x + 22, y + 10,
                fill=c, outline="#dd88ff", width=2
            ))
            # HP bar
            bw = 34
            bh = 4
            self.parts.append(self.canvas.create_rectangle(
                x - bw, y - 30, x + bw, y - 26,
                fill="#222", outline=""
            ))
            self.parts.append(self.canvas.create_rectangle(
                x - bw, y - 30, x - bw + bw * 2 * hp_ratio, y - 26,
                fill=C_GREEN, outline=""
            ))
            self.parts.append(self.canvas.create_oval(
                x - 7, y - 7, x + 7, y + 7,
                fill="#880088", outline="#dd88ff"
            ))

    def update(self):
        self.wobble_tick += 1
        wx = math.sin(self.wobble_tick * 0.05) * (2 if self.kind == self.KIND_FAST else 0.8)
        self.x += wx
        self.y += self.speed
        self._draw()
        return self.y > GAME_H + 30

    def hit(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
        self._draw()
        return self.hp <= 0

    def destroy(self):
        for p in self.parts:
            self.canvas.delete(p)
        self.parts = []

    def should_shoot(self):
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(80, 200)
            return True
        return False

    def rect(self):
        r = 20 if self.kind == self.KIND_TANK else 14
        return (self.x - r, self.y - r, self.x + r, self.y + r)


class Boss(Enemy):
    def __init__(self, canvas, level=1):
        self.canvas = canvas
        self.x = GAME_W // 2
        self.y = -80
        self.kind = "boss"
        self.alive = True
        self.parts = []
        self.shoot_timer = 40
        self.wobble_tick = 0
        self.dx = 1.5
        self.max_hp = 15 + level * 5
        self.hp = self.max_hp
        self.speed = 1.2 + level * 0.15
        self.score = 2000 + level * 500
        self.coins = 100 + level * 30
        self.xp = 200
        self.phase = 1
        self.entering = True
        self._draw()

    def _draw(self):
        for p in self.parts:
            self.canvas.delete(p)
        self.parts = []
        x, y = self.x, self.y
        hp_r = self.hp / self.max_hp
        c1, c2 = C_ENEMY_BOSS, "#aa0033"

        # Large body
        self.parts.append(self.canvas.create_polygon(
            x,       y + 45,
            x - 50,  y + 15,
            x - 50,  y - 15,
            x - 25,  y - 35,
            x,       y - 50,
            x + 25,  y - 35,
            x + 50,  y - 15,
            x + 50,  y + 15,
            fill=c1, outline="#ff4488", width=2
        ))
        # Wing fins
        self.parts.append(self.canvas.create_polygon(
            x - 50, y + 10,
            x - 70, y + 30,
            x - 50, y + 40,
            fill=c2, outline="#880022"
        ))
        self.parts.append(self.canvas.create_polygon(
            x + 50, y + 10,
            x + 70, y + 30,
            x + 50, y + 40,
            fill=c2, outline="#880022"
        ))
        # Cockpit eye
        self.parts.append(self.canvas.create_oval(
            x - 14, y - 24, x + 14, y + 6,
            fill="#ff0055", outline="#ff88aa", width=2
        ))
        self.parts.append(self.canvas.create_oval(
            x - 7, y - 17, x + 7, y - 3,
            fill="#ffddee", outline=""
        ))
        # Cannons
        for cx in [x - 35, x + 35]:
            self.parts.append(self.canvas.create_rectangle(
                cx - 5, y + 10, cx + 5, y + 38,
                fill="#880022", outline="#ff4488"
            ))
        # HP bar
        bw = 60
        self.parts.append(self.canvas.create_rectangle(
            x - bw, y - 58, x + bw, y - 52,
            fill="#330000", outline="#ff0044"
        ))
        self.parts.append(self.canvas.create_rectangle(
            x - bw, y - 58, x - bw + bw * 2 * hp_r, y - 52,
            fill=C_RED, outline=""
        ))
        self.parts.append(self.canvas.create_text(
            x, y - 70, text="⚠ BOSS", fill=C_RED,
            font=("Courier New", 12, "bold")
        ))

    def update(self):
        if self.entering:
            self.y += self.speed
            if self.y >= 100:
                self.entering = False
        else:
            self.x += self.dx
            if self.x >= GAME_W - 80 or self.x <= 80:
                self.dx = -self.dx
        self._draw()
        return False  # boss never exits naturally

    def should_shoot(self):
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            rate = 25 if self.phase == 2 else 40
            self.shoot_timer = rate
            return True
        return False

    def bullet_positions(self):
        """Return list of (x, y) positions to shoot from."""
        if self.hp < self.max_hp * 0.4 and self.phase == 1:
            self.phase = 2
        if self.phase == 1:
            return [(self.x - 35, self.y + 38), (self.x + 35, self.y + 38)]
        else:
            return [(self.x - 35, self.y + 38), (self.x, self.y + 45), (self.x + 35, self.y + 38)]

    def rect(self):
        return (self.x - 50, self.y - 50, self.x + 50, self.y + 45)


# ─────────────────────────────────────────────────────────────
# Game Engine
# ─────────────────────────────────────────────────────────────
class GameEngine:
    TICK = 16  # ~60fps

    def __init__(self, canvas, profile, on_gameover, on_level_up):
        self.canvas = canvas
        self.profile = profile
        self.on_gameover = on_gameover
        self.on_level_up = on_level_up

        # State
        self.running = False
        self.level = 1
        self.score = 0
        self.kills = 0
        self.coins_collected = 0
        self.total_session_kills = 0
        self.boss_killed_ever = False
        self.no_damage_this_level = True

        # Objects
        self.stars = []
        self.player = None
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.boss = None
        self.coins = []
        self.explosions = []
        self.float_texts = []

        # Timing
        self._after_id = None
        self._shoot_ready = True
        self._last_shoot = 0
        self._spawn_timer = 0
        self._level_kills = 0
        self._level_kills_needed = 0
        self._enemies_in_wave = 0

        # Input
        self.keys = set()

        # Applied items from inventory
        self.active_items = {}
        self._load_inventory()

    def _load_inventory(self):
        """Check what items player has in inventory and set modifiers."""
        # Will be called with item data from shop if provided
        pass

    def apply_item(self, item_type, item_id, effect):
        """Apply a consumable item effect."""
        self.active_items[item_type] = {"id": item_id, "effect": effect}
        if item_type == "weapon" and effect == 2.0:
            self.player.shoot_mode = "double"
        elif item_type == "weapon" and effect == 3.0:
            self.player.shoot_mode = "triple"
        elif item_type == "weapon" and effect == 5.0:
            self.player.shoot_mode = "laser"
        elif item_type == "defense":
            self.player.shield = int(effect)
        elif item_type == "movement":
            self.player.speed = int(PLAYER_SPEED * effect)
        elif item_type == "life":
            self.player.lives += 1

    def start(self, canvas_widget, key_press, key_release):
        """Bind keys and start game loop."""
        canvas_widget.bind("<KeyPress>", lambda e: self.keys.add(e.keysym))
        canvas_widget.bind("<KeyRelease>", lambda e: self.keys.discard(e.keysym))
        canvas_widget.focus_set()

        # Init stars
        for _ in range(STAR_COUNT):
            self.stars.append(Star(self.canvas))

        # Init player
        self.player = Player(self.canvas)

        # Start level 1
        self._start_level(1)
        self._loop()

    def _start_level(self, lvl):
        self.level = lvl
        kills_needed, base_speed, spawn_ms, has_boss = LEVELS.get(lvl, (60, 5.0, 700, True))
        self._level_kills_needed = kills_needed
        self._level_kills = 0
        self._base_speed = base_speed
        self._spawn_interval = spawn_ms
        self._has_boss = has_boss
        self._boss_spawned = False
        self._boss_dead = False
        self._spawn_timer = 0
        self.no_damage_this_level = True

        # Clear leftover enemies
        for e in self.enemies:
            e.destroy()
        self.enemies.clear()
        if self.boss:
            self.boss.destroy()
            self.boss = None

        # Show level banner
        lid = self.canvas.create_text(
            GAME_W // 2, GAME_H // 2,
            text=f"LEVEL {lvl}", fill=C_ACCENT,
            font=("Courier New", 36, "bold")
        )
        self.canvas.after(1500, lambda: self.canvas.delete(lid))

        if self.on_level_up:
            self.on_level_up(lvl)

    def _loop(self):
        if not self.running:
            return
        try:
            self._update()
            self._after_id = self.canvas.after(self.TICK, self._loop)
        except tk.TclError:
            self.running = False

    def _update(self):
        import time
        now = time.time() * 1000

        # ── Stars ──
        for s in self.stars:
            s.update()

        # ── Player input ──
        dx = dy = 0
        if "Left" in self.keys or "a" in self.keys:
            dx -= 1
        if "Right" in self.keys or "d" in self.keys:
            dx += 1
        if "Up" in self.keys or "w" in self.keys:
            dy -= 1
        if "Down" in self.keys or "s" in self.keys:
            dy += 1
        if dx or dy:
            self.player.move(dx, dy)

        # Shoot
        delay = SHOOT_DELAY // 2 if self.player.rapid_fire else SHOOT_DELAY
        if "space" in self.keys and now - self._last_shoot >= delay:
            self._shoot_player()
            self._last_shoot = now

        self.player.update()

        # ── Spawn enemies ──
        self._spawn_timer += self.TICK
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0
            if not self._boss_spawned:
                # Check if time for boss
                if self._has_boss and self._level_kills >= self._level_kills_needed and not self._boss_spawned:
                    self._spawn_boss()
                elif self._level_kills < self._level_kills_needed:
                    self._spawn_enemy()

        # ── Update enemies ──
        for e in list(self.enemies):
            gone = e.update()
            if gone:
                e.destroy()
                self.enemies.remove(e)
                continue
            if e.should_shoot():
                self._enemy_shoot(e)

        # ── Boss ──
        if self.boss:
            self.boss.update()
            if self.boss.should_shoot():
                for bx, by in self.boss.bullet_positions():
                    b = Bullet(self.canvas, bx, by, E_BULLET_SPEED, is_enemy=True)
                    self.enemy_bullets.append(b)

        # ── Update bullets ──
        for b in list(self.bullets):
            b.update()
            if not b.alive:
                self.bullets.remove(b)

        for b in list(self.enemy_bullets):
            b.update()
            if not b.alive:
                self.enemy_bullets.remove(b)

        # ── Collision: player bullets vs enemies ──
        for b in list(self.bullets):
            if not b.alive:
                continue
            br = b.rect()
            # vs enemies
            for e in list(self.enemies):
                if not e.alive:
                    continue
                if self._overlap(br, e.rect()):
                    b.destroy()
                    if b in self.bullets:
                        self.bullets.remove(b)
                    killed = e.hit()
                    if killed:
                        self._kill_enemy(e)
                    break
            # vs boss
            if self.boss and b.alive:
                if self._overlap(br, self.boss.rect()):
                    b.destroy()
                    if b in self.bullets:
                        self.bullets.remove(b)
                    killed = self.boss.hit()
                    if killed:
                        self._kill_boss()

        # ── Collision: enemy bullets vs player ──
        for b in list(self.enemy_bullets):
            if not b.alive:
                continue
            if self._overlap(b.rect(), self.player.rect()):
                b.destroy()
                self.enemy_bullets.remove(b)
                dead = self.player.take_hit()
                self.no_damage_this_level = False
                if dead:
                    self._game_over()
                    return

        # ── Collision: enemies vs player ──
        for e in list(self.enemies):
            if not e.alive:
                continue
            if self._overlap(e.rect(), self.player.rect()):
                e.destroy()
                self.enemies.remove(e)
                dead = self.player.take_hit()
                self.no_damage_this_level = False
                if dead:
                    self._game_over()
                    return

        # ── Coins ──
        for c in list(self.coins):
            c.update()
            if not c.alive:
                self.coins.remove(c)
                continue
            if self._overlap(c.rect(), self.player.rect()):
                self.coins_collected += c.value
                ft = FloatText(self.canvas, c.x, c.y, f"+${c.value}", C_GOLD)
                self.float_texts.append(ft)
                c.destroy()
                self.coins.remove(c)

        # ── Explosions ──
        for ex in list(self.explosions):
            ex.update()
            if not ex.alive:
                self.explosions.remove(ex)

        # ── Float texts ──
        self.float_texts = [ft for ft in self.float_texts if ft.update()]

        # ── Level completion ──
        if not self._boss_spawned and self._level_kills >= self._level_kills_needed and not self._has_boss:
            self._next_level()
        elif self._boss_dead:
            self._next_level()

    def _shoot_player(self):
        x, y = self.player.x, self.player.y - 28
        mode = self.player.shoot_mode
        if mode == "single":
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED))
        elif mode == "double":
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED, spread=-8))
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED, spread=8))
        elif mode == "triple":
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED))
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED, spread=-12))
            self.bullets.append(Bullet(self.canvas, x, y, -BULLET_SPEED, spread=12))
        elif mode == "laser":
            for ly in range(y, -20, -40):
                self.bullets.append(Bullet(self.canvas, x, ly, -BULLET_SPEED))

    def _spawn_enemy(self):
        x = random.randint(30, GAME_W - 30)
        kind_roll = random.random()
        if self.level >= 4 and kind_roll < 0.25:
            kind = Enemy.KIND_TANK
        elif self.level >= 2 and kind_roll < 0.55:
            kind = Enemy.KIND_FAST
        else:
            kind = Enemy.KIND_BASIC
        spd = self._base_speed * random.uniform(0.85, 1.15)
        e = Enemy(self.canvas, x, -30, kind, spd)
        self.enemies.append(e)

    def _spawn_boss(self):
        self._boss_spawned = True
        self.boss = Boss(self.canvas, self.level)
        bid = self.canvas.create_text(
            GAME_W // 2, GAME_H // 2 - 40,
            text="⚠ BOSS INCOMING ⚠", fill=C_RED,
            font=("Courier New", 20, "bold")
        )
        self.canvas.after(2000, lambda: self.canvas.delete(bid))

    def _enemy_shoot(self, e):
        b = Bullet(self.canvas, e.x, e.y + 20, E_BULLET_SPEED, is_enemy=True)
        self.enemy_bullets.append(b)

    def _kill_enemy(self, e):
        e.destroy()
        if e in self.enemies:
            self.enemies.remove(e)
        pts = int(e.score * (1 + (self.level - 1) * 0.1))
        self.score += pts
        self.kills += 1
        self.total_session_kills += 1
        self._level_kills += 1
        ex = Explosion(self.canvas, e.x, e.y)
        self.explosions.append(ex)
        ft = FloatText(self.canvas, e.x, e.y - 20, f"+{pts}", C_ORANGE)
        self.float_texts.append(ft)
        # Drop coin
        if random.random() < 0.7:
            coin_val = e.coins
            self.coins.append(Coin(self.canvas, e.x, e.y, coin_val))

    def _kill_boss(self):
        if self.boss:
            ex = Explosion(self.canvas, self.boss.x, self.boss.y, size=3.0)
            self.explosions.append(ex)
            pts = self.boss.score
            self.score += pts
            self.kills += 1
            self.total_session_kills += 1
            self.boss_killed_ever = True
            for _ in range(8):
                cx = self.boss.x + random.randint(-40, 40)
                cy = self.boss.y + random.randint(-30, 30)
                self.coins.append(Coin(self.canvas, cx, cy, self.boss.coins // 8))
            ft = FloatText(self.canvas, self.boss.x, self.boss.y - 60, f"+{pts} BOSS KILL!", C_PINK)
            self.float_texts.append(ft)
            self.boss.destroy()
            self.boss = None
            self._boss_dead = True

    def _next_level(self):
        if self.level >= MAX_LEVEL:
            self._game_over(victory=True)
            return
        self._start_level(self.level + 1)

    def _game_over(self, victory=False):
        self.running = False
        if self._after_id:
            self.canvas.after_cancel(self._after_id)
        self.on_gameover(
            score=self.score,
            level=self.level,
            kills=self.total_session_kills,
            coins=self.coins_collected,
            victory=victory,
            boss_killed=self.boss_killed_ever,
        )

    @staticmethod
    def _overlap(r1, r2):
        return not (r1[2] < r2[0] or r1[0] > r2[2] or
                    r1[3] < r2[1] or r1[1] > r2[3])
