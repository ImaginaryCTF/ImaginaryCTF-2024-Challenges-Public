# The Amazing Race
**Category:** Web
**Difficulty:** Easy/Medium
**Author:** puzzler7

## Description

I've hidden my flag in an impenetrable maze! Try as you might, even though it's right there, you'll never get the flag!

## Distribution

- url

## Solution

There is a race condition where the server first checks if the player can move, then moves the player, then updates whether or not the player can move. This means that by submitting many simultaneous requests to move the same direction at the same time, you can move multiple spaces in a direction that you would normally only be able to move space in, allowing you to tunnel through walls.

See x.py for a partial solution.
