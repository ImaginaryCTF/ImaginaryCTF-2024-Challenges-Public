#!/bin/sh

sed -e "s/\[| (\*MAZE\*) |\]/$(cat maze.txt)/" -e "s/\"\"(\*FLAG\*)/$(cat flag.enc.txt)/" bin/main.ml