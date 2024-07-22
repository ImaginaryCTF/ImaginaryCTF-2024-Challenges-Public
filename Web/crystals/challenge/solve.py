from pwn import *

conn = remote("localhost", 10001)

conn.sendline("""GET /? XTTP/1.1
Host: 127.0.0.1
Connection: close""")

conn.interactive()
