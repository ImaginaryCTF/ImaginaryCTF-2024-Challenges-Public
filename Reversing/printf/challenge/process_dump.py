from pwn import *
from ctypes import CDLL

base = 0x0000555555554000
a = open("dump", "rb").read()
libc = CDLL(None)

def rand64():
  return libc.rand() + (libc.rand() << 32)

out = b""
for i in range(0, len(a), 8):
  if a[i:i+8] == b"\0"*8:
    out += p64(u64(a[i:i+8]) ^ rand64())
  else:
    out += p64((u64(a[i:i+8])+0x0000555555554000) ^ rand64())

print(out.hex())
