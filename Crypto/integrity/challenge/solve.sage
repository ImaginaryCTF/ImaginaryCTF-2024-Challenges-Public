from Crypto.Util.number import *

exec(open("out.txt").read())

def attack(n, e1, c1, e2, c2):
    g, u, v = xgcd(e1, e2)
    p1 = pow(c1, u, n) if u > 0 else pow(pow(c1, -1, n), -u, n)
    p2 = pow(c2, v, n) if v > 0 else pow(pow(c2, -1, n), -v, n)
    return int(ZZ(int(p1 * p2) % n).nth_root(g))

for i in range(65536):
  try:
    a = long_to_bytes(attack(n, 65537, ct, i, signature))
    if b"ictf" in a:
      print(a)
      break
  except:
    pass
