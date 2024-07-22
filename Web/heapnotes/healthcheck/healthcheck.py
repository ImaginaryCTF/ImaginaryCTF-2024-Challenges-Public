#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"https://localhost/login", verify=False).text
  if "Login" in r:
    exit(0)
  else:
    print(r)
    exit(1)
except Exception as e:
  print(e)
  exit(1)
