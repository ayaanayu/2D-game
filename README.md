# NEBULA DEFENDER

A browser-playable 2D space shooter, with the original Python/Pygame version retained in `pygame/`.

## Play in your browser

The website entry point is `index.html`. It uses HTML Canvas and JavaScript, with no build step or external assets required.

### Deploy on Vercel

Import this repository into Vercel and use these settings:

- **Framework Preset:** Other
- **Root Directory:** `./`
- **Build Command:** leave empty
- **Output Directory:** leave empty (or `.` if the dashboard requires a value)

Vercel should serve the root `index.html` as a static site. The Python/Pygame source is inside `pygame/` and is not a Vercel serverless function.

## Browser controls

- Move: `A` / `D` or left/right arrows
- Shoot: `SPACE`
- Pause/resume: `P`
- Start/restart: `ENTER`
- Touch devices: on-screen left, right and fire controls

## Browser game features

- Three enemy types with distinct speed, health and score values
- Increasing difficulty and enemy spawn rate
- Three lives and temporary invulnerability after a hit
- Rapid-fire, shield and extra-health power-ups
- Boss encounter at 120 points
- Starfield, glowing projectiles, particle explosions and screen shake
- Menu, pause, game-over, restart and locally saved high score
- Responsive canvas and touch controls

## Original Python/Pygame edition

The desktop version is kept in:

```
pygame/
├── main.py
└── requirements.txt
```

Run it locally with Python 3:

```bash
python -m pip install -r pygame/requirements.txt
python pygame/main.py
```

Pygame requires a graphical display; a standard browser terminal does not automatically display its game window.

## Repository structure

```
2D-game/
├── index.html
├── README.md
└── pygame/
    ├── main.py
    └── requirements.txt
```
