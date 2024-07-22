#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"http://localhost:5000/").text
  if "Log in" in r:
    exit(0)
  else:
    print("err")
    exit(1)
except Exception as e:
  print(e)
  exit(1)
