import solvelinmod
import random

ords = [random.getrandbits(64) for n in range(4)]
flag = b"ictf"
out = 0
for m,n in zip(ords,flag):
  out += m*n
out %= 2**64

#ords = [14256968251852713, 5856782038711004, 13348175324113344, 8795510881355283]


x0 = var('x0')
x1 = var('x1')
x2 = var('x2')
x3 = var('x3')
#eq = (ords[0]*x0 + ords[1]*x1 + ords[2]*x2 + ords[3]*x3 == 4522333535772311031)
eq = (ords[0]*x0 + ords[1]*x1 + ords[2]*x2 + ords[3]*x3 == out)
bounds = {x0: 2**8, x1: 2**8, x2: 2**8, x3: 2**8}

sol = solvelinmod.solve_linear_mod([(eq, 2**64)], bounds)
print(f'{sol = }')
