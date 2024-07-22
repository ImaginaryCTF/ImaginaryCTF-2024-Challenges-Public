import os

secret_key = os.urandom(256).hex()
aes_key = os.urandom(256).hex()
conn_string = "mongodb://localhost:27017"
