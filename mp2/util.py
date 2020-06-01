"""
# Symmetric key encryption utilities

Follows "the Special Encryption" routine from Pass and Shelat
(Algorithm 157.2)
"""
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import random


def random_bytes(n):
    return os.urandom(n)

KEYLENGTH = 128; # n from Course in Cryptography textbook

def generate_key():
    return random_bytes(KEYLENGTH//8)


def lengthQuadruplingPRF(k, r):
    # Input: 16 byte key, 16 byte value
    # Output: 64 byte pseudorandom bytes
    assert len(k) == KEYLENGTH//8
    assert len(r) <= KEYLENGTH//8
    obj = AES.new(k, AES.MODE_CTR, counter=Counter.new(128))
    output = obj.encrypt(r*4)
    return output

"""
## Problem 0.1: Special Encryption (10 points)

From Pass and Shelat  (Course in Cryptography)
Implement the algorithm from the textbook. Use the provided 
`specialDecryption` function for clarification.
"""

def specialEncryption(k, m):
    assert len(k) == KEYLENGTH//8
    assert len(m) <= KEYLENGTH//8 * 3  # m must be bounded in size

    # TODO: Your code goes here

def specialDecryption(k, c):
    assert len(k) == KEYLENGTH//8
    assert len(c) > KEYLENGTH//8 * 2

    r = c[:KEYLENGTH//8]
    cip = c[KEYLENGTH//8:]

    # Compute the PRF
    prf = lengthQuadruplingPRF(k, r)

    # XORing the message
    assert len(cip) <= len(prf)
    msg = b''.join( bytes([a^b]) for (a,b) in zip( cip, prf ) )

    # Split into two
    pad = msg[:KEYLENGTH//8]
    m = msg[KEYLENGTH//8:]

    # Check the padding
    if pad != b'\x00'*(KEYLENGTH//8): return None
    return m


if __name__ == '__main__':
    # Test vectors for special encryption
    import random
    k = generate_key()
    for i in range(1000):
        l = random.randint(16,48)
        m = random_bytes(l)
        assert specialDecryption(k, specialEncryption(k, m)) == m
