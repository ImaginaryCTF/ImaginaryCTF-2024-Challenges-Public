import struct

with open('output.bin', 'rb') as f:
    data = f.read()

mat = loads(open('matrix.dump', 'rb').read()).inverse()

# numbers = list(struct.unpack('<' + 'i' * 64, data))
numbers = list(struct.unpack('<' + 'b' * 64, data))

chars = []

for i in range(0, 64, 16):
    v = vector(numbers[i:i+16])
    chars += list(mat * v)

print(bytes(chars).decode())
