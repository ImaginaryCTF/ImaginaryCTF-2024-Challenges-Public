# Left in the Dark
**Category**: Misc
**Difficulty**: Easy/Medium
**Author**: puzzler7

# Description
In another challenge, I made a "beautiful" frontend for this maze, but what if you didn't have any of that?

BONK.

# Distributions
- `challenge/maze.py`
- Remote connection, in the form
```sh
socat FILE:`tty`,raw,echo=0 TCP:localhost:1337
```

# Solution

Walking around the maze keeping the wall on your left (or right) is guaranteed to bring you to the flag, if the maze is solvable. See `x.py` for an example

