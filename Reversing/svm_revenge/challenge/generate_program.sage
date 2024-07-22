program = []

for i in range(1, 17):
    program.append('POP')
    program.append(str(i))

# program.append('TRAP')
# program.append('0')

mat = None

while mat is None or gcd(mat.determinant(), 256) != 1:
    mat = matrix.random(Zmod(256), 16)

with open('matrix.dump', 'wb') as f:
    f.write(dumps(mat))

for i, row in enumerate(mat):
    initer = []
    # initer.append('TRAP')
    # initer.append(str(i + 1))
    c = 0
    for j, n in enumerate(row, start=1):
        if n == 0:
            continue
        c += 1
        initer.append('PUSH')
        initer.append(str(j))
        initer.append('PUSH_IMM')
        initer.append(str(n))
    reducer = []
    for j in range(c):
        reducer += ['MUL', str(randint(0, 127))]
    for j in range(c - 1):
        reducer += ['ADD', str(randint(0, 127))]
    program += initer + reducer + ['POP', str(i + 17)]

for i in range(1, 17):
    program.append('PUSH')
    program.append(str(i + 16))

program.append('HALT')
program.append('0')

with open('program.h', 'wt') as f:
    f.write(f"static uint8_t PROGRAM[] = {{ {', '.join(program)} }};")
