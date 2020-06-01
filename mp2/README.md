Machine Problem 2: Garbled Circuits
===================================
This is the second machine problem for ECE/CS 498 AC Applied Cryptography at the University of Illinois at Urbana-Champaign. http://soc1024.ece.illinois.edu/teaching/ece498ac/fall2019/

In this assignment you will need to implement Yao's Garbled Circuits protocol for secure two-party computation.

A two-party computation scheme lets Alice and Bob evaluate functions over their secret inputs. Alice to provide a secret input `a`, Bob to provide a secret input `b`, and at the end of the protocol both parties learn `f(a,b)` and nothing else.

More details about the protocol, and the format of the code in this repository, are included in a PDF handout, `handout.pdf`

The skeleton code includes regions clearly marked `#TODO` that you must fill out to complete the assignment. The number of points associated with each portion is given in the file.

Submitting your solution
------------------------

To submit your solution:
- The due date is (**SEE THE COURSE WEBSITE**)
- You must upload your `mp2` folder as a zip file to Piazza
- The upload must be marked "visible to Instructors"
- The `mp2` folder must contain a text file `report.txt`, which must include a short english-language narrative explaining:
- your net id
- what parts you finished, attempted, couldn't figure out
- any parts you found interesting, challenging, questions you have
- length can be one paragraph, or several... this is not an essay, but it may be used to justify partial credit
- **No partners are allowed for this machine problem.** You must do your own work on this MP.
- Only modify the `evaluator.py`, `generator.py`, `util.py`, and `simpleOT.py` files, since that is the only code we'll check'
- Each script must run (and be able to be imported) without throwing exceptions
- You'll get points for every one of the included tests that passes (though the tests in the file are not comprehensive)
	
Instructions for running
========================

## Install pycryptodome if you don't already have it. Note use pip for python3
```
pip install pycryptodome==3.4.3
```

## To evaluate a simple circuit JSON file on sample inputs
```
python3 circuit.py example_circuits/circuit.json
```

If everything went well, you should expect to see the following output:
```
reading circuit...
[{w7=0}]
```
This means the output wire named `w7` has a 0 value.

You can modify the `example_circuits/circuit.json` file to try out different input values.

## Testing the 32-bit Adder circuit
We provide a python script, run_adder.py, to help you evaluate an example circuit (the 32-bit adder) on numeric inputs. You provide it with the name of the JSON file, and two numeric inputs (decimal numbers). The python script converts the decimal numbers to bits, and writes the bits into the JSON file.

```
python3 run_adder.py <example_circuits/32adder.json> <x> <y>
```

## To execute the Garbled Circuit Evaluator
As you implement your tasks in `evaluator.py`, you can use the following command to execute Bob's role, the circuit evaluator (this will print an error until you implement something!):
```
python3 evaluator.py <garbled.json>
```
We include the `gar_circuit.json` file as an example of a garbled circuit JSON file generated from our reference implementation. After you implement your own Garbled Circuit Evaluator, you can change this filename to point to your own generated files as well.


## To execute the Garbled Circuit Generator
As you implement your tasks in `generator.py`, you can use the following command to execute Alice's role, the circuit generator (this will print an error until you implement something!):
```
python3 generator.py <example_circuits/circuit.json> <garbled.json>
```
where `garbled.json` is used as an output file

## To test your generated circuit files with the reference evaluator
We provide a precompiled (pyz file) implementation of the garbled circuit evaluator. You can run this to check if your garbled circuit implementation matches ours exactly.
```
./obfuscated_evaluator.pyz <./gar_circuit.json>
```

## To give a fuzz test (on random inputs)
```
python3 ./test_garbled_circuit.py <example_circuits/circuit.json>
```

Note: please don't go out of your way to decompile the .pyz!
