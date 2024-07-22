from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
from zlib import crc32

# io = process(['python3', 'server.py'])
io = remote('34.147.35.216', 1337)

io.sendlineafter(b'> ', b'E')
io.sendlineafter(b': ', b'abc')
packet = bytes.fromhex(io.recvline().split(b': ')[-1].decode())

nonce = packet[:8]
checksum = bytes_to_long(packet[8:12])
ciphertext = packet[12:]

mod = b'\x00' * len('{"user": "') + xor(b'user', b'root') + b'\x00' * len('", "command": "') + xor(b'abc", ', b'flag",') + b'\x00' * len('"nonce": "XXXXXXXXXXXXXXXX"}')
forged_ciphertext = xor(ciphertext, mod)
forged_crc = checksum ^ crc32(mod) ^ crc32(b'\x00' * len(mod))
forged_packet = nonce + long_to_bytes(forged_crc) + forged_ciphertext

io.sendlineafter(b'> ', b'R')
io.sendlineafter(b': ', forged_packet.hex().encode())
log.info(io.recvline().decode())
