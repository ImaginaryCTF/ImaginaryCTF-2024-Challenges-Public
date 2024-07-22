from pwn import *

enc = b"lfqc~opvqZdkjqm`wZcidbZfm`fn`wZd6130a0`0``761gdx"
print(xor(enc, 5))
