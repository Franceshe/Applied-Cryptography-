#!/usr/bin/sage

import struct
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto import Random
from math import ceil
from base64 import b64encode, b64decode

### Encoding multi precision integers ###

# Our "MPI" format consists of 4-byte integer length l followed by l bytes of binary key
def int_to_mpi(z):
    assert type(z) is int
    s = z.to_bytes(ceil(z.bit_length() / 8), byteorder='big')
    return struct.pack('I',len(s))+s

# Read one MPI-formatted value beginning at s[index]
# Returns value and index + bytes read.
def parse_mpi(s,index):
    length = struct.unpack('I',s[index:index+4])[0]
    z = int.from_bytes(s[index+4:index+4+length], byteorder='big')
    return z, index+4+length

# Flip all bits in a binary string
def flip_all_bits(s):
    # arg: each character of s is '0' or '1'
    return ''.join('1' if c == '0' else '0' for c in s)


### Message formatting ###
encrypt_header = b'-----BEGIN PRETTY BAD ENCRYPTED MESSAGE-----\n'
encrypt_footer = b'-----END PRETTY BAD ENCRYPTED MESSAGE-----\n'

# PKCS 7 pad message.
def pad(s,blocksize=AES.block_size):
    n = blocksize-(len(s)%blocksize)
    return s+bytes([n])*n

def unpad(msg):
    n = msg[-1]
    return msg[:-n]


### Encryption ###

# Encrypt string s using RSA encryption with AES in CBC mode.
# Generate a 128-bit symmetric key, encrypt it using RSA with
# padding, and prepend the MPI-encoded RSA ciphertext to the
# AES-encrypted ciphertext of the message.
def encrypt(rsakey,s):
    # Generate a 128-bit symmetric key k
    k = random.randint(0,2**128)

    ## PBP-v1.0
    ## Broken code below! Don't use!!!!
    ## This 1.0 version of encryption is really bad,
    ##     it corresponds to Enc(k) = k^3 % N
    ## which can easily be solved for using integer root finding.
    
    # encrypted_key = int_to_mpi(rsakey.encrypt(m))

    ## PBP-v2.0 (fixed)
    ## The more secure version is here. This padding scheme does:
    ## 1. First it ensures the same number of bits are set,
    ##     by concatenating k2 = k || ~k,
    ##    where ~k is all the bits of k flipped
    ## 2. It sets k3 = k2 || k2 || k2 || k2,
    ##    reching about 1024 bits by printing it 4 times

    # Convert to binary
    k_bin = format(k, '0128b')
    assert len(k_bin) == 128

    k2 = k_bin + flip_all_bits(k_bin)
    assert len(k2) == 256

    # Pad it to ~1024-bits by printing x 4 times
    k3 = k2 + k2 + k2 + k2
    assert len(k3) == 1024

    # Encrypt as an integer using rsa
    c = int(rsakey.encrypt(int(k3,2), None)[0])
    encrypted_key = int_to_mpi(c)

    # Use m for symmetric key encryption
    aeskey = k.to_bytes(length=16, byteorder='big')
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    output = encrypted_key + iv + cipher.encrypt(pad(s))

    return encrypt_header + b64encode(output) + b'\n' + encrypt_footer


### Decryption ###

# Decrypt string s using RSA encryption with AES in CBC mode.
def decrypt(rsakey, s):
    # Remove header
    data = re.search(encrypt_header+b"(.*)"+encrypt_footer,s,flags=re.DOTALL).group(1)
    data = b64decode(data)

    # Split into rsa encryption c and symmetric encryption (iv, cipher)
    c, index = parse_mpi(data,0)
    iv = data[index:index+AES.block_size]
    ciphertext = data[index+AES.block_size:]

    # Import the private key
    rsakey = RSA.importKey(open('key.pem').read())

    # Decrypt the symmetric key
    k3 = rsakey.decrypt(c)
    aeskey = k3.to_bytes(128,'big')[:16]

    # Perform symmetric encryption
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))


if __name__=='__main__':
    # Step 1: Make this file run on your own test case, so you can check the
    #         method on examples under your control

    # TODO: create your own keys  so you can run the test file
    pubkey = RSA.importKey(open('key.pub').read())

    plaintext = b"hello world"
    ciphertext = encrypt(pubkey,plaintext)

    ## The commented code below is how the challenge file was encrypted
    plaintext = open('mp4-ece498ac-fall2019.pdf','rb').read()
    ciphertext = encrypt(pubkey,plaintext)
    out_filename = 'mp4-ece498ac-fall2019.enc.asc'
    print('writing %s' % out_filename)
    f = open(out_filename, 'wb')
    f.write(ciphertext)
    f.close()

    # Test decryption, just to show that it works
    seckey = RSA.importKey(open('key.pem').read())
    pt2 = decrypt(seckey, ciphertext)
    assert pt2 == plaintext
    # print("ciphertext:", ciphertext)
    # print("plaintext:", plaintext)
