#!/usr/bin/env python3

from subprocess import Popen
from time import sleep

mazeId = "29f43f1a-294c-49fc-bef1-285af4f8a148"
# Can tunnel through walls in specified direction if there's at least
# one empty space before the wall
#
# Run, readjust position/direction as desired, repeat until flag
url = f"http://localhost:80/move?id={mazeId}&move=down"

for i in range(50):
    Popen(["curl", "-X", "POST", url])
    sleep(.00)
