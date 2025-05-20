# Solitaire Game

This repository contains a minimal command-line implementation of Klondike Solitaire written in Python. It requires Python 3.11 or newer.

## Running the game

```bash
python3 -m solitaire.main
```

Once running, type `draw` to draw from the stock or `move <src> <dest> [count]` to move cards between piles.
Use pile names:
- `waste` or `stock`
- `f1`..`f4` for foundation piles
- `t1`..`t7` for tableau columns

Type `quit` to exit the game.
