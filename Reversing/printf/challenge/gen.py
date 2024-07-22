import random
from pwn import *

regs = ["L", "h", "l", "#", " ", "-", "+", "'"]

opcodes = {
"inp": "A",
"pr": "B",
"pushi": "M",
"pushr": "N",
"pop": "E",
"add": "F",
"sub": "G",
"mul": "H",
"idiv": "I",
"mod": "J",
"xor": "K",
"ex": "X",
"dbg": "?",
}

def i2op(instr, arg=None, reg=None):
  idx = random.randint(1, 5)
  top = arg >> 32 if arg!=None else random.getrandbits(29)
  bottom = arg % 0x100000000 if arg!=None else random.getrandbits(29)
  r = regs[reg] if reg!=None else random.choice(regs)
  opcode = opcodes[instr]
  if instr == "pushi":
    r = ""
  if r in ["#", " ", "-", "+", "'"]:
    return f"%{idx}${r}{top}.{bottom}{opcode}"
  else:
    return f"%{idx}${top}.{bottom}{r}{opcode}"

def compile(asm):
  out = ""
  for instr in asm.strip().split("\n"):
    instr = instr.strip().split()
    if instr[0].startswith("#"):
      continue
    if len(instr) == 1:
      a = i2op(instr[0])
    elif len(instr) == 2 and instr[0] in ["pushi", "dbg"]:
      a = i2op(instr[0], arg=int(instr[1]))
    elif len(instr) == 2:
      a = i2op(instr[0], reg=int(instr[1]))
#    print(instr, a)
    out += a
  return out

def pr(msg):
  out = ""
  for char in msg:
    out += f"""
pushi 2
{build_number((random.getrandbits(50)<<9) + ord(char)*2)}
idiv 0
pushr 0
pr
""".strip() + "\n"
  return out

# gen seed
gen_seed = '''
pushi 2779108660271026260
pushi 8492750646795272566
pushi 2462455873947635985
pushi 4059049647450301267
xor 0
pop 1
pop 1
pushr 0
xor 0
pop 1
pop 1
pushr 0
xor 0
pop 1
pop 1
pushr 0
'''

rng_increment = f'''
pushi 2255327472310680740
mul 0
pop 1
pop 1
pushr 0
pushi 9116454204002618355
add 0
pop 1
pop 1
pushr 0
'''

def check_quad(flag):
  rands = [0, 0, 0, 0x9d29cb475e41cb8f, 0xdd11c039fe5f588f, 0x54ccfb02994249cf, 0x9715552a8c24bd9f, 0x9de3f8582e267573]
  i = random.randint(3,7)
  n = [random.getrandbits(64) for _ in range(4)]
  answer = 0
  for f,m in zip(flag, n):
    answer += f*m
  out = f'''
inp
{build_number(n[0])}
mul 0
pop 1
pop 1
pushr 0
inp
{build_number(n[1])}
mul 0
pop 1
pop 1
pushr 0
inp
{build_number(n[2])}
mul 0
pop 1
pop 1
pushr 0
inp
{build_number(n[3])}
mul 0
pop 1
pop 1
pushr 0
add 2
pop 1
pop 1
pushr 2
add 2
pop 1
pop 1
pushr 2
add 2
pop 1
pop 1
pushr 2
pushr {i}
xor 0
pop 1
pop 1
pushr 0
{build_number(rands[i] ^ answer)}
xor 0
ex
'''
  return out

def build_number(num):
  out = ""
  out += f"pushi {num & 0x7fffffff}\n"
  out += f"pushi {num & 0x7fffffff00000000}\n"
  out += f"add 0\n"
  out += f"pop 1\n"
  out += f"pop 1\n"
  out += f"pushr 0\n"
  if num & (0x80000000):
    out += f"pushi 2\n"
    out += f"pushi {0x80000000>>1}\n"
    out += f"mul 0\n"
    out += f"pop 1\n"
    out += f"pop 1\n"
    out += f"pushr 0\n"
    out += f"add 0\n"
    out += f"pop 1\n"
    out += f"pop 1\n"
    out += f"pushr 0\n"
  if num & (0x8000000000000000):
    out += f"pushi 2\n"
    out += f"pushi {0x8000000000000000>>1}\n"
    out += f"mul 0\n"
    out += f"pop 1\n"
    out += f"pop 1\n"
    out += f"pushr 0\n"
    out += f"add 0\n"
    out += f"pop 1\n"
    out += f"pop 1\n"
    out += f"pushr 0\n"
  return out.strip()

print(compile(pr("""
-------------------------------------
     WELCOME TO THE PRINTF VAULT
-------------------------------------
Enter the flag:""".strip() + " ")))
print(compile(gen_seed))
for i in [7, 6, 5, 4, 3]:
  print(compile(rng_increment))
  print(compile(f"pop {i}"))
  print(compile(f"pushr {i}"))

flag = b"ictf{n3v3r_too_m4ny_form4t_sp3cifi3rs_9a7837294d1633140433f51d13a033736}"

for i in range(0, len(flag), 4):
  print(compile(check_quad(flag[i:i+4])))

print(compile(pr("Correct flag!\n")))
