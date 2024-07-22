#!/usr/bin/env python3

from pwn import *
from random import choice
from console.utils import wait_key

MAZE_SIZE = 40

maze = [['?' for i in range(MAZE_SIZE)] for j in range(MAZE_SIZE)]

maze[0][0] = '.'
maze[MAZE_SIZE-1][MAZE_SIZE-1] = '.'
loc = [0, 0]

p = remote("localhost", 1337)
p.recvline()
p.recvline()
p.recv(timeout=1)

def move(mv):
    global p
    p.send(mv)
    rc = p.recv(timeout=.05)
    if b'ictf' in rc:
        print(rc)
        exit()
    # print(rc)
    return not bool(rc)

def u():
    ret = move(b'w')
    if ret:
        loc[0] -= 1
        maze[loc[0]][loc[1]] = '.'
    elif loc[0] > 0:
        maze[loc[0]-1][loc[1]] = '#'
    return ret

def d():
    ret = move(b's')
    if ret:
        loc[0] += 1
    elif loc[0] < MAZE_SIZE - 1:
        maze[loc[0]+1][loc[1]] = '#'
    return ret

def r():
    ret = move(b'd')
    if ret:
        loc[1] += 1
    elif loc[1] < MAZE_SIZE - 1:
        maze[loc[0]][loc[1]+1] = '#'
    return ret

def l():
    ret = move(b'a')
    if ret:
        loc[1] -= 1
    elif loc[1] > 0:
        maze[loc[0]][loc[1]-1] = '#'
    return ret

def pm():
    maze[loc[0]][loc[1]] = '@'
    print('\n'.join(''.join(row) for row in maze))
    maze[loc[0]][loc[1]] = '.'
    print()

dirs = [r, d, l, u]
facing = 0
while True:
    pm()
    turned = dirs[facing-1]()
    if turned:
        facing -= 1
        facing %= 4
        continue
    forward = dirs[facing]()
    if forward:
        continue
    facing += 1
    facing %= 4
