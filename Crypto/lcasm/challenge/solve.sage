from pwn import *
import solvelinmod

a = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05\x00"
nums = []
for n in range(0, len(a), 8):
  nums.append(u64(a[n:n+8]))

print(nums)

mod = 2**64-3
a = var('a')
c = var('c')
eq2 = nums[1]*-1 + nums[0]*a + 1*c == 0
eq3 = nums[2]*-1 + nums[1]*a + 1*c == 0
bounds = {a: 2**62, c: 2**62}
sol = solvelinmod.solve_linear_mod([(eq2, mod), (eq3, mod)], bounds)
print(f'{sol = }')

a = ( int(sol[a]) + mod ) % mod
c = ( int(sol[c]) + mod ) % mod

x = (((nums[0] - c) % mod) * pow(a, -1, mod)) % mod
print(f"{x = }")
print(f"{a = }")
print(f"{c = }")
print(f"{mod = }")

conn = remote("35.204.162.128", int(1337))
#conn = process("./lcasm")

x = 6549227833016977563
a = 15634179043583660018
c = 10769788045638517834
mod = 18446744073709551613

conn.sendline(str(x).encode())
conn.sendline(str(a).encode())
conn.sendline(str(c+3).encode()) # i have no idea why this works
conn.sendline(str(mod).encode())
conn.interactive()
