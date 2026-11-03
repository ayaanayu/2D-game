# NEBULA DEFENDER

A self-contained 2D space shooter made with Python 3 and Pygame. All artwork is drawn at runtime; no external art/audio files are needed.

## Run in GitHub Codespaces

```bash
python -m pip install -r requirements.txt
python main.py
```

Pygame needs a graphical display. A standard browser terminal does not automatically display Pygame windows; use a GUI-enabled Codespaces environment/desktop forwarding or run locally.

## Controls

- Move: `A` / `D` or left/right arrows
- Shoot: `SPACE`
- Pause/resume: `P` (or `ESC`)
- Start/restart: `ENTER`
- Tablet/mobile: on-screen left, right and fire buttons; mouse input also works.

## Features

- Three enemy types with distinct speed, health and score values
- Increasing spawn rate and difficulty as score rises
- Three lives and temporary invulnerability after a hit
- Rapid-fire, shield and extra-health power-ups
- Boss encounter at 120 points
- Starfield, glowing projectiles, particle explosions and screen shake
- Menu, pause, game-over, restart and locally saved high score
- Resizable window and delta-time movement

## Project structure

```
2D-game/
├── main.py
├── requirements.txt
└── README.md
```

## Customize

Edit the configuration constants near the top of `main.py`:

| Constant | Effect |
|---|---|
| `PLAYER_SPEED` | Player movement speed |
| `BULLET_SPEED` | Player projectile speed |
| `PLAYER_LIVES` | Starting and maximum health |
| `ENEMY_BASE_SPEED` | Base enemy movement speed |
| `ENEMY_SPAWN_BASE` | Initial spawn interval (lower = harder) |
| `BOSS_SCORE` | Score threshold for boss |
| `BOSS_HEALTH` | Boss starting health |

Enemy stats are in `Enemy.SPECS`. Power-up durations are in `Player.update()` and `PowerUp.apply()`.

The high score is saved to `~/.nebula_defender_highscore` on the machine running the game. Audio is omitted so the game has no sound-device dependency.
