
with open("chal.txt", "wb") as f:
  f.write(bytes.fromhex('FEFF'))
  for n in b"ictf{th4t_isn7_chin3se}":
    f.write(bytes([n]))
f.close()
