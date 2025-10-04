# Console Snake Game

A simple snake game playable in the terminal, implemented in Python.

## Features

- Playable in the console with WASD controls
- Random food generation (`$`)
- Score tracking (snake length)
- High score tracking (stored in `highscore.txt`)
- Game over detection (collision with wall `#` or snake body)
- Works on Windows, Linux, and Mac
- Cursor hiding for better gameplay experience
- Option to restart or exit after game over or pressing `K`

## Requirements

- Python 3.x
- [`keyboard`](https://pypi.org/project/keyboard/) library

Install dependencies with:

```sh
pip install keyboard
```

## How to Run

```sh
python snake.py
```

## Controls

- `W` - Move Up
- `A` - Move Left
- `S` - Move Down
- `D` - Move Right
- `K` - Quit

## Gameplay

- Eat `$` to grow the snake.
- Avoid hitting the walls (`#`) or the snake's own body.
- Your score is the length of the snake.
- High scores are saved in `highscore.txt`.
- After game over or pressing `K`, you can choose to restart or exit.

## Notes

- The game uses terminal cursor manipulation; best played in a standard terminal.
- On some systems, running as administrator/root may be required for keyboard input.
- The cursor is hidden during gameplay and restored when the game ends.
- The terminal is cleared at the start of each game for better visibility.
