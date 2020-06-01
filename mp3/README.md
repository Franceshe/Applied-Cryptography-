Machine Problem 3: Multiparty Computation
=========================================
This is the third machine problem for ECE/CS 498 AC Applied Cryptography at the University of Illinois at Urbana-Champaign. http://soc1024.ece.illinois.edu/teaching/ece498ac/fall2019/

In this assignment you will implement shamir's secret sharing and several
approaches for computing on secret shared data.

More details about the protocol, and the format of the code in this repository, are included in a PDF handout, `handout.pdf`

The skeleton code includes regions clearly marked `#TODO` that you must fill out to complete the assignment. The number of points associated with each portion is given in the file.

Setup
------------------------
You will need to install pycryptodome, gevent for the assignment. Note this is to be completed in `python3` 
`pip install pycryptodome --user`
`pip install gevent --user`

Submitting your solution
------------------------

To submit your solution:
- The due date is (**SEE THE COURSE WEBSITE**)
- You must upload your `mp3` folder as a zip file to Piazza. The folder **must** be named `mp3`. 
- The upload must be marked "visible to Instructors"
- The `mp3` folder **must** contain a text file `report.txt`, which must include a short english-language narrative explaining:
- your net id
- what parts you finished, attempted, couldn't figure out
- any parts you found interesting, challenging, questions you have
- length can be one paragraph, or several... this is not an essay, but it may be used to justify partial credit
- **No partners are allowed for this machine problem.** You must do your own work on this MP.
- Only modify the `polynomials.py`, `mpc_sim.py`, `secretsharing.py`, and `fouriertransform.py` files, since that is the only code we'll check'
- Each script must run (and be able to be imported) without throwing exceptions
- You'll get points for every one of the included tests that passes (though the tests in the file are not comprehensive)