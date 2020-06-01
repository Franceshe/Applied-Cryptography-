import json
from collections import defaultdict, deque

class BooleanCircuit(object):

    def __init__(self, from_json=None):
        self.gates = {}
        self.wires = {}

        if from_json is not None:
            # Construct the circuit from a json object
            assert type(from_json) is dict

            # Receives its value from...
            wires = set()
            
            output_map = {} # wire id => gate id
            input_map = defaultdict(set)
            
            gates = from_json["gates"]
            for gid in gates: # gate ids
                gate = gates[gid]

                # Right now, only support 2-in and 1-out gates
                assert len(gate["inp"]) == 2
                assert len(gate["out"]) == 1
                
                # Each gate must be associated with either an op or a table
                assert "type" in gate or "table" in gate
                if "type" in gate:
                    assert gate["type"] in ("AND","XOR","OR")
                    # Fill table from pre-recorded function
                    table = { "AND" : [0,0,0,1],
                              "XOR" : [0,1,1,0],
                              "OR"  : [0,1,1,1] }[gate["type"]]
                    if "table" in gate: assert table == gate["table"]
                else:
                    table = gate["table"]
                assert len(table) == 4
                assert all([v in (0,1) for v in table])

                # Collect the input/output wires
                inp = gate["inp"]
                wires.update(inp)
                for i in inp:
                    input_map[i].add(gid)

                # Set the output wire
                out = gate["out"]
                wires.update(gate["out"])
                assert out[0] not in output_map
                output_map[out[0]] = gid

                self.gates[gid] = dict(out=out, inp = gate["inp"], table=table)
            self.wires = wires
            self.input_map = dict(input_map)
            self.output_map = output_map
            self.input_wires = wires.difference(output_map)
            self.output_wires = wires.difference(input_map)

            # Do the topological sort
            self._topological_sort()

    def _topological_sort(self):
        # Precondition: 
        # Postcondition: self.sorted_gates is a topological sort of gate ids
        
        # 1. Initialize a mutable table of pending inputs
        inputs_pending = {}
        for gid,gate in list(self.gates.items()):
            inputs_pending[gid] = set(gate["inp"]) # 

        # Mark all the input wires
        for wid in self.input_wires:
            for gid in self.input_map[wid]:
                inputs_pending[gid].remove(wid)

        # Initialize a queue of resolvable gates
        q = deque()
        for gid in self.gates:
            if len(inputs_pending[gid]) == 0: q.append(gid)

        # 2. Loop by grabbing a resolvable vertex
        wires_processed = len(self.input_wires)
        sorted_gates = []
        while wires_processed < len(self.wires):
            assert len(q) != 0, "Stuck. A cycle must be present"
            gid = q.popleft()
            sorted_gates.append(gid)
            # Mark the output wire of this gate as resolved
            out = self.gates[gid]["out"][0]
            wires_processed += 1
            # Update all inputs_pending for all gates with this input
            if out not in self.input_map: continue # output wire
            for g in self.input_map[out]:
                inputs_pending[g].remove(out)
                if len(inputs_pending[g]) == 0: q.append(g)

        self.sorted_gates = sorted_gates

    def evaluate(self, inp):
        # Precondition: initialized, topologically sort
        # Postcondition: self.wire_values takes on values resulting from this evaluation
        # Takes an array of bits as input
        assert len(inp) == len(self.input_wires)
        wire_values = dict( (wid,None) for wid in self.wires )
        for wid,v in list(inp.items()):
            assert v in (0,1)
            wire_values[wid] = v

        for gid in self.sorted_gates:
            gate = self.gates[gid]
            a = wire_values[gate["inp"][0]]
            b = wire_values[gate["inp"][1]]
            c = gate["table"][2*a + b]
            wire_values[gate["out"][0]] = c

        self.wire_values = wire_values

        return dict((wid,wire_values[wid]) for wid in self.output_wires)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: python circuit.py <circuit.json>")
        sys.exit(1)

    filename = sys.argv[1]
    obj = json.load(open(filename))

    # Circuit
    c = BooleanCircuit(from_json=obj)
    print(('Circuit loaded: %d gates, %d input wires, %d output_wires, %d total' \
        % (len(c.gates), len(c.input_wires), len(c.output_wires), len(c.wires))))

    # inputs
    if "inputs" in obj:
        print("Inputs found")
        inputs = obj["inputs"]
        assert len(inputs) == len(c.input_wires)
        output = c.evaluate(inputs)
        print(("Output:", output))

