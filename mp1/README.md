Machine Problem 1: Zero Knowledge Proofs
========================================
This is the first machine problem for ECE/S 498 AM Applied Cryptography at the University of Illinois at Urbana-Champaign. http://soc1024.ece.illinois.edu/teaching/ece498ac/fall2019/

In this assignment you will need to implement several zero-knowledge proof schemes for languages involving discrete logarithms. This assignment is intended to provide:
1. a hands-on way to understand "group theory". 
2. practice implementing variations of a cryptographic protocol
3. reinforcement of the concepts behind analyzing a protocol with "security proofs" (You will have to implement in code the "Simulator" and the "Extractor" that make up part of the proof).

The expression `ZkPoK { (x): X = g^X }` in Camenisch-Stadler notation means a proof that you know a secret witness `x` such that `X = g^x`, where `X` is a publicly known value (called the statement) and `g` is a generator of a large cyclic group.

In class, we've discussed the Schnorr protocol for creating interactive proofs for this language, as well as "Sigma Protocol" variants for other language (arithmetic constraints, "OR" proofs, etc.), and how to make such protocols non-interactive using a random oracle (the Fiat-Shamir trick).

This assignment uses a specific commonly used cryptographic group, `secp256k1` (found in Bitcoin, for example). The assignment provides an example implementation of the basic scheme. It also provides skeleton code for incrementally more complicated variations (roughly following the lectures), and a few simple test cases for each. 

The implementation of `secp256k1` used here is due to Jeremy Kun, who has a fantastic series of blogposts explaining modular arithmetic, finite fields, and elliptic curves. https://jeremykun.com/2014/03/19/connecting-elliptic-curves-with-finite-fields-a-reprise/ The python files in this assignment can be converted to .ipynb using `pynb`

The skeleton code ( `zkp-assignment.py/` ) includes regions clearly marked `#TODO` that you must fill out to complete the assignment. The number of points associated with each portion is given in the file. 

Submitting your solution
------------------------

To submit your solution:
- The due date is (**SEE THE COURSE WEBSITE**)
- You must upload your `mp1` folder as a zip file to Piazza
- The upload must be marked "visible to Instructors"
- The `mp1` folder must contain a text file `report.txt`, which must include a short english-language narrative explaining:
  - your net id
  - what parts you finished, attempted, couldn't figure out
  - any parts you found interesting, challenging, questions you have
  - length can be one paragraph, or several... this is not an essay, but it may be used to justify partial credit
- **No partners are allowed for this machine problem.** You must do your own work on this MP.
- Only modify the `zkp-assignment.py` file, since that is the only code we'll check
- The file must run without throwing exceptions
- You'll get points for every one of the included tests that passes (though the tests in the file are not comprehensive)
