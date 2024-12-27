import sys
import random

# in this approach, we will re-write the input file to be more readable...

def getInput():
    if len(sys.argv) < 2:
        print("Please pass file name")
        sys.exit(1)
    part1 = True
    gates = []
    with open(sys.argv[1]) as file:
        for line in file:
            if len(line) < 2:
                part1 = False
            elif not part1:
                parts = line.split()
                gates.append((parts[1], parts[0], parts[2], parts[4]))
    return gates

# always put the x part on the left
def swapXY(gates):
    for i in range(len(gates)):
        g = gates[i]
        if g[1][0] == "y" and g[2][0] == "x":
            gates[i] = (g[0], g[2], g[1], g[3])

def replaceWire(gates, a, b):
    for i in range(len(gates)):
        g = gates[i]
        new = [g[0], g[1], g[2], g[3]]
        if g[0] == a:
            new[0] = b
        if g[1] == a:
            new[1] = b
        if g[2] == a:
            new[2] = b
        if g[3] == a:
            new[3] = b
        gates[i] = tuple(new)

# rename the xi ^ yi gates to be si
def identifySums(gates):
    reps = []
    # find them all first
    for i in range(len(gates)):
        g = gates[i]
        if g[1][0] == "x" and g[2][0] == "y" and g[0] == "XOR":
            reps.append((g[3], "s" + g[1][1:]))
    # replace them all
    for rep in reps:
        replaceWire(gates, rep[0], rep[1])

def dump(gates):
    for gate in gates:
        print(gate[1], gate[0], gate[2], "->", gate[3])

gates = getInput()
swapXY(gates)
identifySums(gates)
dump(gates)


