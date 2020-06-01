"""
# Zero Knowledge Proofs in Python

Examples of discrete-log zero-knowledge proofs implemented in Python

More specifically, these are non-interactive, zero-knowledge,
proofs of knowledge. They can be analyzed and proven secure
in the random oracle model (the random oracle here is instantiated
with the SHA2 hash function).

Lecture notes:
   http://soc1024.ece.illinois.edu/teaching/ece498am/fall2017/
   https://www.cs.jhu.edu/~susan/600.641/scribes/lecture10.pdf
   https://www.cs.jhu.edu/~susan/600.641/scribes/lecture11.pdf
   http://soc1024.web.engr.illinois.edu/teaching/ece598am/fall2016/zkproofs.pdf

You must fill in the portions labelled #TODO. See the README.md in this
directory for submission instructions. Points are awarded as marked.
Total possible points: 100
"""


"""
## Import Elliptic Curves

The zero-knowledge proof schemes we work through here
 can work with any DLog group. This implementation makes use of
the secp256k1 elliptic curve group. We call an element of this group
(i.e., a point on the curve), simply a Point.

The order of this group, p, is a 256-bit prime number. Furthermore, p
happens to be extremely close to 2^256. Because of this, we can sample
exponents easily by choosing a random 32-byte number, and with high probability,
will be within [0,p).
   uint256_from_str(rnd_bytes(32)) is an exponent.

Sometimes this will be represented by the object Fp, which automatically handles
arithmetic modulo p. The underlying 'long' value can be extracted as `p.n` if 
`type(p) is Fp`.
"""

import secp256k1
from secp256k1 import Point, q, Fq, order, p, Fp, G, curve, ser, deser, uint256_from_str, uint256_to_str
import os, random

# p is the order (the # of elements in) the group, i.e., the number of points on the curve
# order = p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
print(order)
print(Fp)  # Fp is the group of exponents (integers mod p)

# ser/deser: convert Point -> string and vice versa
#   ser : Point -> str, deser : str -> Point

"""
"""
print(repr(G))
print(repr(p * G))
print(deser(ser(G)))

Hx = Fq(0x4d81249b749d3cb7641cd8522f5e1a45b6bd8db03f20d6b96d5077c84d2c053f)
Hy = Fq(0xf39272d1d9a4cca99bcce01590b7e8355bd2fafec94dd10f9e0c98f6cb5be8fa)
H = Point(curve, Hx,Hy)
# H = random_point(seed=sha2("H")) # An alternate generator


"""
## Random Oracle Functions
We need ways of sampling random strings, random integers in Z_p,
and random points in the group.
"""

## Default random oracle
def make_random_oracle():
    """This function returns a new random oracle, `RO`.
    The random oracle maps arbitrary-length input strings `s` to
    a 32-byte digest. It is initialized with an empty dictionary. 
    Each time RO is queried with a new value, a
    random response is sampled and stored."""
    
    _mapping = {}
    def RO(s):
        assert type(s) is str
        if not s in _mapping:
            _mapping[s] = os.urandom(32)
        return _mapping[s]
    return RO

## Map a string to a random value in Zp
def random_oracle_string_to_Zp(s):
    return sha2_to_long(s) % p

#Find sha2 hash of a string
def sha2(x):
    from Crypto.Hash import SHA256
    return SHA256.new(x.encode("utf-8")).digest()

def sha2_to_long(seed):
    from Crypto.Hash import SHA256
    return int(SHA256.new(seed).hexdigest(),16)

## Pick a random point on the curve (given a seed)
def random_point(seed=None, rnd_bytes=os.urandom):
    if seed is None: seed = rnd_bytes(32)
    # assert type(seed) == str and len(seed) == 32
    x = sha2_to_long(seed)
    while True:
        try:
            p = secp256k1.solve(Fq(x))
        except ValueError:
            seed = sha2(('random_point:' + str(seed)))
            x = sha2_to_long(seed)
            continue
        break
    return p

print(random_point(sha2("hi")))
"""
_Question:_ can we figure out the discrete log of `random_point("hi")`?
  That is, find the scalar `a` such that `a * G == random_point("hi")`?
"""


"""
## Preliminary example: Proof of knowledge of discrete logarithm

In this part, we provide a scheme offers a discrete log proof of `ZKP{ (a): A = a*G }`.

Note that the statement `A` is a parameter to the scheme, as it must
be known to both the prover and verifier.

The Prover takes several additional arguments:

 - `rnd_bytes`, such that `rnd_bytes(n)` returns an `n`-byte random string. By default, will use the operating system os.urandom. 

    (Note: as this function is non-blocking, may be a poor choice if the OS runs out of entropy)

 - RO, a random oracle, such that `RO(s)` where `s` is an arbitrary length string, returns a randomly chosen value. By default, will use the sha2 hash.

These can be overridden in later section as part of the security proof constructions.
"""
def dlog_prover(A, a, rnd_bytes=os.urandom, RO=sha2):
    assert a*G == A

    # blinding factor
    k = uint256_from_str(rnd_bytes(32)) % order

    # commitment
    K = k*G

    # Invoke the random oracle to receive a challenge
    c = uint256_from_str(RO(ser(K)))

    # response
    s = Fp(k + c*a)

    return (K,s)


def dlog_verifier(A, prf, RO=sha2):
    (K,s) = prf
    assert type(A) is type(K) is Point
    assert type(s) is Fp

    # Recompute c w/ the information given
    c = uint256_from_str(RO(ser(K)))

    # Check the verification condition
    assert s.n *G == K + c*A
    return True


def dlog_test():
    a = uint256_from_str(os.urandom(32))
    A = a*G
    prf = dlog_prover(A, a)
    assert dlog_verifier(A, prf)
    print('Dlog correctness test complete!')

dlog_test()

"""
## Part 1: Make a Pedersen commitment to your crypto egg. 
 Provide a ZK proof that your commitment is correct.

   Zk{ (x,r): X = x*G, C = x*G + r*H }

By completing this proof, you prove you still have knowledge of your egg!
without revealing which.

The verifier is provided for you. (Since we will publicly verify the proofs). You must complete the prover.
"""

def make_pedersen_commitment(x, rnd_bytes=os.urandom):
    r = uint256_from_str(rnd_bytes(32))
    C = x * G + r * H
    return C, r

def pedersen_prover(C, X, x, r, rnd_bytes=os.urandom, RO=sha2):
    """
    Params: 
       x and r are elements of Fp
       C,X are Points
    Returns:
       prf, of the form (KX,KC,sx,sr)
    """
    assert X == x * G
    assert C == x * G + r * H

    # TODO: fill in your code here (10 points)

    return (KX,KC,sx,sr)

def pedersen_verifier(C, X, prf, RO=sha2):
    (KX,KC,sx,sr) = prf
    assert type(KX) == type(KC) == Point
    assert type(sx) == type(sr) == Fp

    # Recompute c w/ the information given
    c = uint256_from_str(RO(ser(KX) + ser(KC)))

    assert sx.n *G            == KX + c*X
    assert sx.n *G + sr.n *H  == KC + c*C
    return True

def pedersen_test():
    x = uint256_from_str(os.urandom(32))
    X = x * G
    C,r = make_pedersen_commitment(x)

    prf = pedersen_prover(C, X, x, r)
    (KX, KC, sx, sr) = prf
    print(repr((ser(C), ser(KX),ser(KC),uint256_to_str(sx.n).hex(),uint256_to_str(sr.n).hex())))

    assert pedersen_verifier(C, X, prf)
    print("Pedersen correctness test complete!")

pedersen_test()


"""
## Part 1 b): Make a single Pedersen commitment to a vector of secrets

   Zk{ (x1...xn,r1...rn): C1 = x1*G + r1*H, C2 = x2*G + r2*H, .. Cn = xn*G + rn*H }

The verifier is provided for you. (Since we will publicly verify the proofs). You must complete the prover.
"""

def pedersen_vector_prover(C_arr, x_arr, r_arr, rnd_bytes=os.urandom, RO=sha2):
    """
    Params: 
       x_arr, r_arr are arrays of elements in Fp
       C_arr are arrays of Points
    Returns:
       prf, of the form (K,sx,sr) where K is points and sx and sr are points in Fp 
       Note that here you are able to prove that knowledge of n points with only communicating 1 ppints and 2 scalars.
    """

    # Make sure all commitments are correct
    for C_elem, x_elem, r_elem in zip(C_arr,x_arr,r_arr):
        assert C_elem == x_elem*G + r_elem*H

    # TODO: Your code goes here: 10 points

def pedersen_vector_verifier(C_arr, prf, rnd_bytes=os.urandom, RO=sha2):
    (C0, sx, sr) = prf

    assert type(C0) == Point
    assert type(sx) == type(sr) == Fp

    c = Fp(uint256_from_str(RO(ser(C0))))
    
    e = c
    C_final = C0
    for C_elem in C_arr:
        C_final = C_final + e.n*C_elem
        e = Fp(e*c)

    assert C_final == sx.n*G + sr.n*H

    return True

def pederson_vector_test():
    x_arr, r_arr, C_arr = [], [], []
    for _ in range(10):
        x_elem = uint256_from_str(os.urandom(32))
        C_elem, r_elem = make_pedersen_commitment(x_elem)
        x_arr.append(x_elem)
        C_arr.append(C_elem)
        r_arr.append(r_elem)

    prf = pedersen_vector_prover(C_arr, x_arr, r_arr)

    assert pedersen_vector_verifier(C_arr, prf)
    print("Pedersen vector correctness test complete!")

pederson_vector_test()

"""
## Part 2. Arithmetic relations

Example: a more complicated discrete log proof
      Zk{ (a, b):  A=a*G, B=b*G,  C = (a*(b-3)) * G }

First rewrite as:
      Zk{ (a, b):  A=a*G, B=b*G,  (C + 3*A) = b*A) }

You need to implement a prover and verifier for the above scheme.
"""

def arith_prover(a, b, A, B, C, rnd_bytes=os.urandom, RO=sha2):
    """
    Params: 
       a and b are elements of Fp
       A, B, C are Points
    Returns:
       prf, of the form (KA,KB,KC,sa,sb)

    Must satisfy verify_proof2(A, B, C, prf)
    Must be zero-knowledge
    """
    assert a*G == A
    assert b*G == B
    assert (a*(b-3))*G == C

    # TODO: fill in your code here (10 points)

def arith_verifier(A, B, C, prf, rnd_bytes=os.urandom, RO=sha2):
    (KA,KB,KC,sa,sb) = prf
    assert type(KA) == type(KB) == type(KC) == Point
    assert type(sa) == type(sb) == Fp

    # TODO: fill in your code here (10 points)

def arith_test():
    # Randomly choose "a" and "b"
    a = uint256_from_str(os.urandom(32))
    b = uint256_from_str(os.urandom(32))
    A = a*G
    B = b*G
    C = (a*(b-3)) * G

    prf = arith_prover(a, b, A, B, C)
    assert arith_verifier(A, B, C, prf)
    print("Arithmetic Relation correctness test complete")

arith_test()

"""
## Part 3. OR composition

In this part you will need to combine two

   Zk{ (a,b): A = a*G    OR    B = b*G }

without revealing which one it is you know.

The verifier is provided for you.
"""

def OR_prover(A, B, x, rnd_bytes=os.urandom, RO=sha2):
    assert x*G == A or x*G == B

    # TODO: Fill your code in here (20 points)

def OR_verifier(A, B, prf, RO=sha2):
    (KA,KB,sa,sb,ca,cb) = prf
    assert type(KA) is type(KB) is Point
    assert type(sa) is type(sb) is Fp

    # Check the challenges are correctly constrained
    c = uint256_from_str(RO(ser(KA) + ser(KB)))
    assert (ca + cb) % p == c

    # Check each proof the same way
    assert sa.n *G == KA + ca*A
    assert sb.n *G == KB + cb*B

    return True

def OR_test1():
    # Try first way
    a = uint256_from_str(os.urandom(32))
    A = a*G
    B = random_point()

    prf = OR_prover(A, B, a)
    assert OR_verifier(A, B, prf)
    print("OR composition correctness 1 test complete!")

def OR_test2():
    # Try second way
    b = uint256_from_str(os.urandom(32))
    A = random_point()
    B = b*G

    prf = OR_prover(A, B, b)
    assert OR_verifier(A, B, prf)
    print("OR composition correctness 2 test complete!")

OR_test1()
OR_test2()


"""
## Part 4. Schnorr signature

  We can write a Schnor signature as:

     SoK[m] { (x): X = x*G }

  Similar to part 1, except we the challenge is derived from the message.
"""
def schnorr_sign(x, m, rnd_bytes=os.urandom, RO=sha2):
    assert type(x) is bytes
    assert type(m) is str

    # TODO: Your code goes here (10 points)

def schnorr_verify(X, m, sig, RO=sha2):
    assert type(X) is Point
    assert type(sig) is bytes and len(sig) is 65
    (K,s) = deser(sig[:33].hex()), uint256_from_str(sig[33:])
    c = uint256_from_str(RO(ser(K) + sha2(m).hex()))
    assert s *G == K + c*X
    return True

def schnorr_test():
    msg = "hello"

    x = os.urandom(32)
    X = uint256_from_str(x) * G
    
    sig = schnorr_sign(x, msg)
    assert schnorr_verify(X, msg, sig)
    print("Schnorr Test complete")

schnorr_test()


"""
## Part 5. Range proofs

- Create a proof that C = g^a*h^r, and a is in the range [0,64).

    Zk{ (a, r): C = g^a*h^r and  0 <= a <= 63 }

  Hint: You can implement this by creating commitments to the binary expansion
    of A, and then proving the following:

    Zk{ (b0, b1, ... b4,b5, r0, r1, ..., r4, r5, r'): A = g^(b0 + 2*b1 + ... + 16*b4 + 32*b5)*g^(r0 + 2*r1 + ... + 16*r4 + 32*r5)*h(r')
                                    and  (C0 = g^(b0) h^r0) ....
                                    and  (C0 = g h^r0 OR C0 = h^r0) ... }
"""
def range_prover(a, r, C, rnd_bytes=os.urandom, RO=sha2):
    assert type(C) is Point
    assert a*G + r*H == C

    # TODO: fill in your code here (10 points)

def range_verifier(C, prf, rnd_bytes=os.urandom, RO=sha2):
    assert type(C) is Point

    # TODO: fill in your code here (10 points)


"""
## Part 6: Extractor and simulator

In this part, you will implement in code a portion of the security proof
for the discrete log proof scheme from the Preliminary.
"""
def dlog_extractor(A, Adv):
    assert type(A) is Point

    ## Step 1: run the adversary to generate a proof while recording
    ## the random bits and oracle queries

    # TODO: Fill your code in here

    ## Step 2: run the adversary again, replaying the random bits,
    ## and intercepting the call to the random oracle

    # TODO: Fill your code in here (5 points)

    ## Step 3: Extract a witness from the two proofs and oracle queries

    # TODO: Fill your code in here (5 points)

def dlog_test_extractor():
    import os
    # Make a test case based on running the real prover
    a = uint256_from_str(os.urandom(32))
    A = a * G
    
    def Adv(A, rnd_bytes, RO):
        assert A == a * G
        return dlog_prover(A, a, rnd_bytes, RO)

    a_ = dlog_extractor(A, Adv)
    assert a == a_
    print('Extractor test complete!')

def dlog_test_extractor_harder():
    # Make a test case based on running a "picky" prover
    a = uint256_from_str(os.urandom(32))
    A = a * G

    def Adv(A, rnd_bytes, RO):
        assert A == a * G

        while True:
            # The "picky" prover loops until it is happy

            # Make a whimsical decision
            coin = rnd_bytes(1)
            if ord(coin) < 128: continue

            k = uint256_from_str(rnd_bytes(32)) % order
            K = k*G
            c = uint256_from_str(RO(ser(K)))

            # I only like challenges that end with 3 zero bits
            if c & 0b111 != 0: continue

            # OK I'm satisfied
            s = Fp(k + c*a)
            return (K, s)

    a_ = dlog_extractor(A, Adv)
    assert a == a_
    print('Extractor test complete!')

dlog_test_extractor()
dlog_test_extractor_harder()

def dlog_simulator(A, rnd_bytes):
    """
    Returns:
    - (prf, transcript)
    - prf, a tuple of the form (K,s),
        where K is a Point
        and s is an element of Fp
    - transcript is an array consisting of elements of the form
        [...(q,h)...]
      where each q is a query (a string)
      and each h is the response (a 32-byte string)
    """
    # TODO: Fill in your code here (10 points)

def dlog_test_simulator():
    rnd_bytes = os.urandom
    # Test with a randomly generated point on curve
    A = random_point(rnd_bytes=rnd_bytes)

    (prf, transcript) = dlog_simulator(A, rnd_bytes)

    # Unpack the proof
    K,s = prf
    assert type(K) is Point
    assert type(s) is Fp

    # Unpack oracle transcript (there should be just one query)
    assert len(transcript) == 1
    (q,h) = transcript[0]

    assert q == ser(K)
    c = uint256_from_str(h)

    # Check the verification condition
    assert s.n *G == K + c*A

    print("DLOG simulator test complete!")

dlog_test_simulator()

