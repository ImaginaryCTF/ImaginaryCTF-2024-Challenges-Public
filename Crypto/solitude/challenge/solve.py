from pwn import *

conn = remote("34.91.117.150", 1337)

def retr(i):
  conn.recvuntil(b"? ")
  conn.sendline(str(i).encode())
  out = []
  out = conn.recvuntil(b"got", drop=True).strip().split()
  return [bytes.fromhex(i.decode()) for i in out]


res = [{} for _ in range(len(retr(1)[0])-1)]
for a in retr(100000):
  for i in range(len(a)-1):
    rr = a[i] ^ a[i+1]
    if rr in res[i]:
      res[i][rr] += 1
    else:
      res[i][rr] = 1

recovered = [max(r.keys(), key=lambda x: r[x]) for r in res]
flag = list(b"i")
for f in recovered:
  flag.append(f ^ flag[-1])
print(bytes(flag))
