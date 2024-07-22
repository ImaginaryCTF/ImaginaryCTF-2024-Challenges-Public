#!/usr/bin/env python3

import requests

try:
  s = requests.Session()
  r = s.get(f"http://localhost:8000/").text
  if "View" in r:
    exit(0)
  else:
    exit(1)
except:
  exit(1)
