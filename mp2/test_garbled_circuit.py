#!/usr/bin/env python
import json,sys
from collections import OrderedDict
import subprocess
from circuit import BooleanCircuit
from evaluator import GarbledCircuitEvaluator
from generator import GarbledCircuitGenerator

import sys
import os
import random
import tempfile

def main():
    if len(sys.argv) != 2:
        print('usage: test_garbled_circuit.py <circuit.json>')
        print('Generates random circuit inputs and tests generator & evaluator')
        sys.exit(1)

    filename = sys.argv[1]
    obj = json.load(open(filename))

    # Load the plain circuit
    plain = BooleanCircuit(from_json=obj) 

    # Generate the garbled circuit
    c = GarbledCircuitGenerator(from_json=obj)
    print('Circuit loaded: %d gates, %d input wires, %d output_wires, %d total' \
        % (len(c.gates), len(c.input_wires), len(c.output_wires), len(c.wires)))

    for i in range(100):

        inputs = dict((wid,random.randint(0,1)) for wid in plain.input_wires)
    
        # Generate the garbled circuit
        c.garble()

        # Possible improvement: Check for statistical evidence of shuffling!!
        with tempfile.NamedTemporaryFile(prefix='garble_', suffix='.json', delete=False) as f:
            f.close()

            # Save the json obj
            c.output(f.name, inputs)

            # Evaluate the garbled circuit
            obj = json.load(open(f.name))
            e = GarbledCircuitEvaluator(from_json=obj)

            garble_inputs = obj["inputs"]

            out_labels = e.garbled_evaluate(garble_inputs)

            # Check correctness
            outs = plain.evaluate(inputs)
            for wid,v in outs.items():
                assert out_labels[wid] == c.wire_labels[wid][v], "output wire mismatch"

            os.remove(f.name)
        

if __name__ == '__main__':
    main()
