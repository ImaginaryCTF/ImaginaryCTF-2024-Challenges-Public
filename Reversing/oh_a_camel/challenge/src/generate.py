from Crypto.Cipher import ARC4, ChaCha20
from hashlib import sha256
from random import choice


def create_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]
    walls = [(1, 0), (0, 1)]
    maze[0][0] = '.'

    while len(walls) > 0:
        wall = choice(walls)
        walls.remove(wall)
        wx, wy = wall

        if wy < 0 or wy >= height or wx < 0 or wx >= width or maze[wy][wx] != '#':
            continue

        if (wx - 1 < 0 or maze[wy][wx - 1] == '.') and wx + 1 < width and maze[wy][wx + 1] == '#':
            if (wy - 1 < 0 or maze[wy - 1][wx] != '.') and (wy + 1 >= height or maze[wy + 1][wx] != '.'):
                maze[wy][wx] = '.'
                maze[wy][wx + 1] = '.'
                walls += [(wx + 1, wy + 1), (wx + 1, wy - 1), (wx + 2, wy)]
            else:
                continue
        elif (wx + 1 >= width or maze[wy][wx + 1] == '.') and wx - 1 >= 0 and maze[wy][wx - 1] == '#':
            if (wy - 1 < 0 or maze[wy - 1][wx] != '.') and (wy + 1 >= height or maze[wy + 1][wx] != '.'):
                maze[wy][wx] = '.'
                maze[wy][wx - 1] = '.'
                walls += [(wx - 1, wy + 1), (wx - 1, wy - 1), (wx - 2, wy)]
            else:
                continue
        elif (wy - 1 < 0 or maze[wy - 1][wx] == '.') and wy + 1 < height and maze[wy + 1][wx] == '#':
            if (wx - 1 < 0 or maze[wy][wx - 1] != '.') and (wx + 1 >= width or maze[wy][wx + 1] != '.'):
                maze[wy][wx] = '.'
                maze[wy + 1][wx] = '.'
                walls += [(wx + 1, wy + 1), (wx - 1, wy + 1), (wx, wy + 2)]
            else:
                continue
        elif (wy + 1 >= height or maze[wy + 1][wx] == '.') and wy - 1 >= 0 and maze[wy - 1][wx] == '#':
            if (wx - 1 < 0 or maze[wy][wx - 1] != '.') and (wx + 1 >= width or maze[wy][wx + 1] != '.'):
                maze[wy][wx] = '.'
                maze[wy - 1][wx] = '.'
                walls += [(wx + 1, wy - 1), (wx - 1, wy - 1), (wx, wy - 2)]
            else:
                continue
        else:
            continue


    return maze


def print_maze(maze):
    for row in maze:
        print(' '.join(row), end='\n\n')


def to_ocaml_repr(maze):
    rows = []

    for row in maze:
        rows.append('[| ' + '; '.join('true' if c == '.' else 'false' for c in row) + ' |]')
    
    return '[| ' + '; '.join(rows) + ' |]'


def solve_maze(maze, result, nodes_on_path=[], current=(0, 0), visited=set()):
    if current == (len(maze[0]) - 1, len(maze) - 1):
        return True

    if current in visited:
        return False

    visited.add(current)
    x, y = current

    for dir, dx, dy in [('L', -1, 0), ('R', 1, 0), ('U', 0, -1), ('D', 0, 1)]:
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= len(maze[0]) or ny >= len(maze) or maze[ny][nx] == '#':
            continue
        if solve_maze(maze, result, nodes_on_path, (nx, ny), visited):
            result.append(dir)
            nodes_on_path.append((nx, ny))
            return True

    return False


def verify_maze_has_one_solution(maze):
    solution = []
    solve_maze(maze, [], solution)

    for x, y in solution[1:]:
        maze[y][x] = '#'
        assert not solve_maze(maze, [])
        maze[y][x] = '.'


width = 65
height = 65
maze = create_maze(width, height)
assert maze[height - 1][width - 1] == '.'

path = []
solve_maze(maze, path)
path = ''.join(path[::-1])

verify_maze_has_one_solution(maze)

print_maze(maze)
print(path)
print(len(path))

with open('maze.txt', 'wt') as f:
    f.write(to_ocaml_repr(maze))

with open('flag.enc.txt', 'wt') as f:
    key = sha256(path.encode()).digest()
    cipher = ChaCha20.new(key=key, nonce=b'deadbeef')
    ct = cipher.encrypt(b'ictf{b3w4r3_0f_tr34ch3r0u5_d353rt5_4nd_t4gg3d_1nt3g3r5!}')
    f.write('"' + repr(repr(ct)[2:-1])[1:-1] + '"')
