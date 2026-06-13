# Tennis Showdown

A single-player Pong-style tennis game built in Python as a final project for **Stanford University's Code in Place** program. Play against a computer opponent and be the first to score 5 points to win.

---

## Gameplay
<img width="346" height="397" alt="Title" src="https://github.com/user-attachments/assets/4428f756-c302-4e3f-9d33-b80e63127f19" />

The ball bounces between two paddles. Where the ball hits your paddle affects the angle it deflects i.e. hitting near the edges sends it off at a sharper angle, giving you control over the rally. The ball also speeds up slightly with each paddle hit, raising the pressure as the match goes on.

---

## Features

- **Title screen** with a tennis icon and Enter-to-start flow
- **5 table-colour options** — Blue, Green, Pink, Grey, Aqua
- **3 difficulty levels** — Easy, Medium, Hard (controls AI paddle speed)
- **Angle-based ball deflection** — impact position on the paddle affects the rebound angle
- **Progressive ball speed** — ball accelerates on each hit, capped at a maximum
- **Live score display** throughout the match
- **Final score shown** on the win/lose screen
- **Restart or quit** from the game-over screen without relaunching the program

---

## Controls

| Key | Action |
|---|---|
| `←` / `→` | Move your paddle |
| `Enter` | Start game / Restart after game over |
| `Escape` | Quit |

---

## How to Run

This project uses the `graphics.py` Canvas library provided by Stanford's Code in Place course.

**Prerequisites:**
- Python 3.x
- `graphics.py`
- Image assets: `tennis icon.png`, `trophy.png`, `sad.png` in the same directory

**Run:**
```bash
python main.py
```

---

## Acknowledgements

Built using the **Code in Place `graphics.py`** library developed by Stanford University.  
Course: [Code in Place](https://codeinplace.stanford.edu/)
