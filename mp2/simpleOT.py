"""
# Problem 3: The Simplest Oblivious Transfer (10 points)

An implementation of 1-of-2 oblivious transfer,
based on the protocol from Chou and Orlandi[1].

The sender starts with two strings M0 and M1.
The receiver starts with a selector bit c
At the end of the protocol, the reciever learns (M0,M1)[c], and that's all.

The protocol is sketched in the following ~20 lines of pseudocode:

Sender:
  Input(M0, M1)
  a <-$-- Fp
  send A = a*G to receiver
  receive B from the sender
  k0 = RO(a * B)
  k1 = RO(a * (B-A))
  e0 = Encrypt(k0, M0)
  e1 = Encrypt(k1, M1)
  send e0, e1 to the receiver

Receiver
  Input(c)    a bit 0 or 1
  b <-$-- Fp
  receive A from sender
  B = b*G if c == 0 else A + b*G
  kR = RO(b*A)
  send B to sender
  receive e0 e1 from the sender
  return Decrypt(kR, e0) if c == 0 else Decrypt(kR, e1)

For concreteness, this implementation encrypts performs 1-of-2 OT over
16-byte strings. (For ease of composition with the Garbled Circuits assignment)

This protocol is UC secure. It relies on a special Encrypt/Decrypt function
which is self-contained here. Briefly, the encryption scheme is 
non-committing and robust, which is what's needed to ensure safe composition.

This protocol relies on the hardness of the Computational Diffie Hellman 
problem. In particular, our implementation uses the secp256k1 elliptic curve.

[1] "The Simplest Protocol for Oblivious Transfer"
Chou and Orlandi. 
https://eprint.iacr.org/2015/267.pdf
"""

import secp256k1
from secp256k1 import Point, q, Fq, order, p, Fp, G, curve, ser, deser, uint256_from_str, uint256_to_str, make_random_point
import os
from Crypto.Hash import SHA256

"""
## The Simplest OT Protocol.
Proceeds in 3 rounds:

Sender(M0,M1)
Receiver(c)

Sender --> Receiver round 1   sends the point A, stores secret a
Sender <-- Receiver round 2   sends the point B, stores secret b
Sender --> Receiver round 3   sends a pair of encryptions e0,e1

The receiver finally decrypts using the key it constructs from b and A.
"""

# Random oracle instantiated with SHA2 hash
def sha2(x):
    return SHA256.new(x.encode("utf-8")).digest()

def sender_round1(rnd_bytes=os.urandom):
    """
    Inputs:
       none
    Returns:
       (a, A)   

       A is sent to receiver, 
       a is stored and passed to sender_round3
    """
    # TODO: Your code goes here
    
    return a, A

def receiver_round2(c, A, rnd_bytes=os.urandom, RO=sha2):
    """
    Inputs:
       c  a bit 0 or 1
       A  the round1 message from the sender
    Returns:
       (kR, B)
       B is sent to the sender,
       kR is the decryption key, stored and passed to sender_round4
    """
    assert c in (0,1)
    assert type(A) is Point

    # TODO: Your code goes here
    return kR, B

def sender_round3(M0, M1, a, B, RO=sha2):
    """
    Inputs:
       M0 and M1, each an element in Fp
       kR: the secret saved from sender_round1
    Returns:
       (e0,e1), the two ciphertexts
    """
    assert type(a) is Fp
    assert type(M0) is bytes and type(M1) is bytes
    assert len(M0) == len(M1) == 16
    # TODO: your code goes here
    return e0, e1    

def receiver_round3(c, kR, e0, e1):
    """
    Use kR to decrypt either e0 or e1, depending on bit c
    """
    assert type(kR) is bytes and len(kR) == 32
    assert c in (0,1)
    # TODO: your code goes here

"""
## Non-committing and one-time  encryption

For UC security, it is necessary to use a non-committing and robust 
one-time encryption scheme. Such a scheme is given as:

  Encrypt(k, m):
    (a,b) = k
    e = (m xor a, b)

  Decrypt(k, e):
    (a,b) = k
    (ma, b_) = e
    assert b_ == b
    return (ma xor a)

  It's just a one-time pad, so it provides information theoretic security.
  The value "b" is effectively just used as a session key.
"""

def strxor(a,b):
    # Computes a ^ b, byte by byte
    assert type(a) is type(b) is bytes
    assert len(a) == len(b), "a and b must be the same size"
    return b''.join( bytes([a ^b]) for (a,b) in zip(a,b))

def encrypt(k, m):
    # This is a non-committing and robust one-time encryption scheme.
    # It's a one-time pad, with some redundancy.
    # It encrypts messages that are exactly 16 bytes, and uses 32-byte keys
    assert len(k) == 32
    assert len(m) == 16
    # parse k as (alpha,beta), 16 bytes each
    alpha = k[:16]
    beta  = k[16:]
    return strxor(alpha,m) + beta

def decrypt(k, c):
    assert len(k) == 32
    assert len(c) == 32
    # parse k as (alpha,beta), 16 bytes each
    alpha = k[:16]
    beta  = k[16:]
    
    if beta != c[16:]: return None  # Decryption fails
    return strxor(alpha,c[:16])
    
"""
## Test case
"""
def test_OT():
    M0 = os.urandom(16)
    M1 = os.urandom(16)

    # Case 0
    c = 0
    a, A = sender_round1()
    kR, B = receiver_round2(c, A)
    e0, e1 = sender_round3(M0, M1, a, B)
    m = receiver_round3(c, kR, e0, e1)
    assert m == M0
    print('Case 0 ok')

    # Case 1
    c = 1
    kR, B = receiver_round2(c, A)
    e0, e1 = sender_round3(M0, M1, a, B)
    m = receiver_round3(c, kR, e0, e1)
    assert m == M1
    print('Case 1 ok')
test_OT()
