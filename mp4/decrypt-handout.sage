import struct
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

def decrypt():
    # Read the file
    s = open('mp4-ece498ac-fall2019.enc.asc','rb').read()

    rsakey = RSA.importKey(open('key.pub').read())

    plaintext = b""

    f = open("mp4-decode.pdf",'wb')
    f.write(plaintext)

if __name__ == "__main__":
    decrypt()
