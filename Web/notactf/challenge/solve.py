from xorCryptPy import xorCrypt
import base64
from pwn import xor
import requests
import os
from hashlib import md5

def __pkcs7_padding(s):
    """
    Padding to blocksize according to PKCS #7
    calculates the number of missing chars to BLOCK_SIZE and pads with
    ord(number of missing chars)
    @see: http://www.di-mgt.com.au/cryptopad.html
    @param s: string Text to pad
    @type s: string
    @rtype: string
    """
    BLOCK_SIZE = 16
    s_len = len(s)
    s = s + (BLOCK_SIZE - s_len % BLOCK_SIZE) * chr(BLOCK_SIZE - s_len % BLOCK_SIZE).encode('utf-8')
    return s

s = requests.Session()
uname = os.urandom(5).hex().upper()
pwd = os.urandom(5).hex()

print(uname, md5(uname.encode()).hexdigest())
s.post("http://34.34.94.246:80/register", data={"username": uname, "password": pwd})
s.post("http://34.34.94.246:80/login", data={"username": uname, "password": pwd})
token = (s.get("http://34.34.94.246:80/home").text.split('"')[-8])

decoded_token = xorCrypt(bytes.fromhex(token).decode(), 938123)

a = base64.b64decode(decoded_token)

second_block = a[32:48]
plain_third_block = __pkcs7_padding(uname.encode())
new_third_block = __pkcs7_padding(b"admin")

new_second_block = xor(second_block, plain_third_block, new_third_block)
new = a[:32] + new_second_block + a[48:]
print(len(a))
print(len(new))
new = base64.b64encode(new).decode()
new_token = xorCrypt(new, 938123).encode().hex()
print(new_token)


headers = {
"user-auth-token": new_token,
#"user-auth-token": token,
"action": "get-challenges",
}
r = s.post("http://34.34.94.246:80/admin", headers=headers)
print(r.text)
