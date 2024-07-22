import random
import sympy

flag="ictf{1_h4t3_3s0l4ng5_7d4f3a1b}"

code=""
equations=[]
for i in flag:
	rand=random.randint(30,70)
	while sympy.isprime(rand):
		rand=random.randint(30,70)
	RHS = eval(f"ord(i)+{rand}")
	equations.append(f"{ord(i)}+{rand}={RHS}")
	factors = sympy.divisors(rand)
	best_factors=[factors[int(len(factors)/2)]]
	best_factors.append(int(rand/best_factors[0]))
	fac1=best_factors[0]
	fac2=best_factors[1]
	assert fac1*fac2==rand
	code += f",>>{'+'*fac1}[<{'+'*fac2}>-]<[-<+>]<{'-'*RHS}[><]"

print(code)
