from pwn import *

conn = remote("35.204.145.12", 1337)
conn.recvuntil(b"> ")

def midpoint(p1, p2):
  p1 = list(map(int, p1.split(",")))
  p2 = list(map(int, p2.split(",")))
  return ",".join(map(str,[(i1+i2)//2 for i1, i2 in zip(p1, p2)]))

def explode(pt):
  return list(map(int, pt.split(",")[:-1]))

# get the target points
conn.sendline(b"4")
conn.recvuntil(b": ")
a = conn.recvuntil(b" ").strip().decode()
conn.recvuntil(b": ")
conn.recvuntil(b": ")
b = conn.recvuntil(b" ").strip().decode()

info("point 1: " + str(a))
info("point 2: " + str(b))

# poison the data
conn.sendline(b"42")
conn.sendline((midpoint(a,b) + ",friendly").encode())

info("poison point: " + midpoint(a,b))

# train the model
conn.sendline(b"2")

# get the flag
conn.sendline(b"4")

conn.interactive()
