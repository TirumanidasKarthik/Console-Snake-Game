# Console Snake Game

A simple snake game playable in the terminal, implemented in Python.

## Features

- Playable in the console with WASD controls
- Random food generation
- Score tracking
- Game over detection (collision with wall)
- Works on Windows, Linux, and Mac

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
- Avoid hitting the walls (`#`).
- Your score is the length of the snake.

## Notes

- The game uses terminal cursor manipulation; best played in a standard terminal.
- On some systems, running as administrator/root may be required for keyboard input.
