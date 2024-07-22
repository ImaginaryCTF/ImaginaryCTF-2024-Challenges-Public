#!/usr/bin/env python3

from flask import Flask, redirect, render_template, Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlite3 import *
from uuid import uuid4
from time import sleep

from maze import Maze

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

MAZE_SIZE = 35

def initDb():
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS mazes(
            id TEXT PRIMARY KEY, 
            maze TEXT NOT NULL,
            row INTEGER NOT NULL DEFAULT 0,
            col INTEGER NOT NULL DEFAULT 0,
            up BOOL NOT NULL DEFAULT False,
            down BOOL NOT NULL DEFAULT True,
            left BOOL NOT NULL DEFAULT False,
            right BOOL NOT NULL DEFAULT True
            )
    ''')
    con.commit()
    cur.close()
    con.close()

def createMaze():
    mazeId = str(uuid4())
    maze = Maze(2, MAZE_SIZE)

    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    cur.execute('''
        INSERT INTO mazes (id, maze)
        VALUES (?, ?)
    ''', (mazeId, str(maze).strip()))
    con.commit()
    cur.close()
    con.close()
    return mazeId

def getMaze(mazeId):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    ret = cur.execute("SELECT maze FROM mazes WHERE id = ?", (mazeId,)).fetchone()[0]
    cur.close()
    con.close()
    return ret

def getLoc(mazeId):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    ret = cur.execute("SELECT row, col FROM mazes WHERE id = ?", (mazeId,)).fetchone()
    cur.close()
    con.close()
    return ret

def getCanMove(mazeId):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    ret = cur.execute("SELECT up, down, left, right FROM mazes WHERE id = ?", (mazeId,)).fetchone()
    cur.close()
    con.close()
    return ret

def writeMaze(mazeId, maze):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    cur.execute('''
        UPDATE mazes SET maze = ? WHERE id = ?
    ''', (maze, mazeId))
    con.commit()
    cur.close()
    con.close()

def writeLoc(mazeId, loc):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    cur.execute('''
        UPDATE mazes SET row = ?, col = ? WHERE id = ?
    ''', (*loc, mazeId))
    con.commit()
    cur.close()
    con.close()

def writeCanMove(mazeId, canMove):
    con = connect("/tmp/mazes.db")
    cur = con.cursor()
    cur.execute('''
        UPDATE mazes SET up = ?, down = ?, left = ?, right = ? WHERE id = ?
    ''', (*canMove, mazeId))
    con.commit()
    cur.close()
    con.close()

def bound(n, mn=0, mx=MAZE_SIZE):
    return max(min(n, mx), mn)

def inn(n, mn = 0, mx = MAZE_SIZE):
    return mn <= n < mx 

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route("/", defaults={"mazeId": None})
@app.route("/<mazeId>")
def index(mazeId):
    if not mazeId:
        return redirect(f"/{createMaze()}")
    solved=getLoc(mazeId) == (MAZE_SIZE-1, MAZE_SIZE-1)
    return render_template("maze.html", 
        maze=getMaze(mazeId), 
        mazeId=mazeId,
        flag=open("flag.txt").read() if solved else ""
    )

@app.route("/source")
def source():
    return Response(open(__file__), mimetype="text/plain")

@app.route("/maze")
def mazeSource():
    return Response(open("maze.py"), mimetype="text/plain")

@app.route("/docker")
def docker():
    return Response(open("Dockerfile"), mimetype="text/plain")

@app.route("/move", methods=["POST"])
def move():
    mazeId = request.args["id"]
    moveStr = request.args["move"]

    canMove = getCanMove(mazeId)
    validMoves = ["up", "down", "left", "right"]
    moveIdx = None
    if moveStr in validMoves:
        moveIdx = validMoves.index(moveStr)
    validMovesDict = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
    move = validMovesDict.get(moveStr, None)
    if not move or moveIdx is None or not canMove[moveIdx]:
        return redirect(f"/{mazeId}")

    currentLoc = getLoc(mazeId)
    newLoc = [bound(currentLoc[0] + move[0]), bound(currentLoc[1] + move[1])]
    writeLoc(mazeId, newLoc)

    mazeStr = getMaze(mazeId)
    maze = [[c for c in row] for row in mazeStr.splitlines()]
    maze[currentLoc[0]][currentLoc[1]] = '.'
    maze[newLoc[0]][newLoc[1]] = '@'
    writeMaze(mazeId, '\n'.join(''.join(row) for row in maze))

    newCanMove = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        checkLoc = [newLoc[0] + dr, newLoc[1] + dc]
        newCanMove.append(
            inn(checkLoc[0]) and inn(checkLoc[1])
            and maze[checkLoc[0]][checkLoc[1]] != '#'
        )
    writeCanMove(mazeId, newCanMove)

    return redirect(f"/{mazeId}")

initDb()
