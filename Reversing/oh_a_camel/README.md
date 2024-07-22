# Oh, a Camel!
**Category:** Reversing
**Difficulty:** Medium/Hard
**Author:** lodsb

## Description

While exploring twisted corridors of an ancient pyramid, you find a weird scroll with a camel drawn on it. You pick it up, but don't have too much time to inspect it...

## Distribution

- output/main.exe

## Solution

Don't reverse the whole thing, realize that the most important part is `camlDune__exe__Main__is_position_legal_84` which checks whether given tile is a wall or not. Dump the whole maze (either by reading the values from the buffer or by using dynamic instrumentation to repeatedly call the function with different coordinates as arguments) and run DFS or BFS to solve it. Send the path to program's stdin and read the flag.
