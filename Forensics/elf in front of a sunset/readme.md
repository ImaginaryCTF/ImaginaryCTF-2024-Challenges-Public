# elf in front of a sunset
**Category:** Forensics
**Difficulty:** Easy-Medium
**Author:** Minerva.

## Description
Here is a picture of elves, taken from Wikipedia. Enjoy.

## Distribution

- `togive/elves.bmp`

## Solution
The size of bitmap image and the pixel count do not match. Fixing the bitmap height from the header data reveals top rows that contain an elf executable encoded in 8 bit grayscale. Extract it, and reverse it to find a shuffled flag as well as the shuffling algorithm. Reverse and submit. 
