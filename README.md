# ✦ NEBULA DEFENDER

**A browser-playable 2D arcade space shooter built with HTML Canvas and JavaScript, with an original Python/Pygame edition included.**

<p align="center">
  <a href="https://2d-game-iota.vercel.app/"><strong>▶ PLAY NEBULA DEFENDER</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/ayaanayu/2D-game">View source code</a>
</p>

---

## About the game

Nebula Defender is a fast-paced arcade space shooter. Pilot your ship, survive increasingly challenging enemy waves, collect power-ups, and take on a powerful boss. The browser edition runs directly from the website—there is no installation or account required to play.

**Play online:** https://2d-game-iota.vercel.app/

## Features

- **Arcade-style combat:** Move your ship and fire twin projectiles at incoming enemies.
- **Three enemy classes:** Scouts, fighters, and tanks with different movement speeds, health, and score values.
- **Progressive difficulty:** Enemy waves become more challenging as your score increases.
- **Boss encounter:** A boss appears when you reach 120 points, with a health bar and projectile attacks.
- **Power-ups:**
  - Rapid Fire — temporarily increases firing speed.
  - Shield — temporarily protects your ship.
  - Health — restores a life, up to the maximum of three.
- **Visual effects:** Animated starfield, glow effects, particle explosions, and screen shake.
- **Game states:** Start menu, pause, game over, and restart.
- **Score tracking:** Current score and a locally saved best score.
- **Responsive play:** Browser canvas adapts to the available screen width, with touch controls on mobile devices.

## How to play

1. Open the [game website](https://2d-game-iota.vercel.app/).
2. Select **Start Game** or press **Enter**.
3. Move your ship, avoid enemy attacks, and shoot incoming enemies.
4. Collect power-ups and try to defeat the boss.
5. Survive as long as possible and beat your best score.

### Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move left | `A` or `←` | Left button |
| Move right | `D` or `→` | Right button |
| Shoot | `Space` | Fire button |
| Pause / resume | `P` | — |
| Start / restart | `Enter` | Start button |

## Tech stack

### Browser edition
- **HTML5** — page structure
- **CSS3** — layout and responsive presentation
- **JavaScript** — game logic, input, animation, and collision handling
- **HTML Canvas API** — real-time 2D rendering
- **Browser local storage** — best-score persistence

The browser edition is self-contained in `index.html`. It does not require a package manager, build process, or external game assets.

### Desktop edition
- **Python 3**
- **Pygame 2**

The original desktop implementation is retained in the `pygame/` directory.

## Run locally

### Option 1: Browser edition

No dependencies are required.

1. Clone the repository:
   ```bash
   git clone https://github.com/ayaanayu/2D-game.git
   cd 2D-game
   ```
2. Open `index.html` in a modern web browser.

For a local development server, you can use the VS Code Live Server extension or run:
```bash
python -m http.server 8000
```
Then visit http://localhost:8000.

### Option 2: Python/Pygame edition

Make sure Python 3 is installed, then run:

```bash
git clone https://github.com/ayaanayu/2D-game.git
cd 2D-game
python -m pip install -r pygame/requirements.txt
python pygame/main.py
```

The Pygame edition opens in a desktop game window and requires a graphical environment.

## Deploy your own copy

The browser edition can be deployed as a static site on [Vercel](https://vercel.com/).

1. Import this GitHub repository into Vercel.
2. Set **Framework Preset** to **Other**.
3. Set **Root Directory** to `./`.
4. Leave **Build Command**, **Install Command**, and **Output Directory** empty.
5. Deploy.

Vercel serves the root `index.html` directly. The Python files are stored under `pygame/` and are not part of the website deployment.

## Repository structure

```text
2D-game/
├── index.html              # Browser game (HTML, CSS, JavaScript)
├── README.md               # Project documentation
└── pygame/
    ├── main.py             # Desktop Pygame edition
    └── requirements.txt    # Python dependencies
```

## Project links

- **Live game:** https://2d-game-iota.vercel.app/
- **GitHub repository:** https://github.com/ayaanayu/2D-game

## Contributing

Suggestions, bug reports, and improvements are welcome. If you find an issue, please open a GitHub issue with steps to reproduce it. For code changes, create a branch and submit a pull request with a clear description of the update.

## License

No license has been specified for this repository yet. Unless a license is added, the source code is publicly viewable but standard copyright restrictions still apply.

---

<p align="center">
  Made as a 2D game development project · <strong>NEBULA DEFENDER</strong>
</p>
