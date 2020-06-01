#!/bin/bash
set -x #echo on

# Snip
python ./snip.py ./zkp-assignment-solution.py ./zkp-assignment.py

# Make ipynb
py2nb ./zkp-assignment.py
py2nb ./secp256k1.py
