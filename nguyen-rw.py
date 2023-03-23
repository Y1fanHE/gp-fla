"""Random Walk for Symbolic Regression Problems

Created by Yifan He (heyif@outlook.com)
Last update on Mar 02, 2023
"""
import operator
import random
import math
import sys
from copy import deepcopy
from deap import base, creator,gp, tools
from benchmarks import SymbolicRegression
from tools import mutLocal, mutLeaf, mutLeafParent


funcs = {
    "2": lambda x: x**4+x**3+x**2+x,
    "6": lambda x: math.sin(x)+math.sin(x+x**2),
    "9": lambda x,y: math.sin(x)+math.sin(y*y),
    "10": lambda x,y: 2*math.sin(x)*math.cos(y),
}

inputs = {
    "2": [(x/10,) for x in range(-10, 10)],
    "6": [(x/10,) for x in range(-10, 10)],
    "9": [(x/5,y/5) for x in range(-5,5) for y in range(-5,5)],
    "10": [(x/5,y/5) for x in range(-5,5) for y in range(-5,5)],
}

sr = SymbolicRegression(
    func=funcs[sys.argv[1]],
    inputs=inputs[sys.argv[1]]
)

i = int(sys.argv[2])
max_count = int(sys.argv[3])
max_tree_height = int(sys.argv[4])

with open(f"run{i}.dat", "w") as log:
    log.close()

def protectedDiv(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 1

def protectedExp(a):
    try:
        return math.exp(a)
    except OverflowError:
        return 1

def protectedLog(a):
    try:
        return math.log(abs(a))
    except ValueError:
        return 0

pset = gp.PrimitiveSet("MAIN", sr.n_inputs, "X")
pset.addPrimitive(operator.add, 2, "ADD")
pset.addPrimitive(operator.sub, 2, "SUB")
pset.addPrimitive(operator.mul, 2, "MUL")
pset.addPrimitive(protectedDiv, 2, "DIV")
pset.addPrimitive(math.sin, 1, "SIN")
pset.addPrimitive(math.cos, 1, "COS")
pset.addPrimitive(protectedExp, 1, "EXP")
pset.addPrimitive(protectedLog, 1, "LOG")
if sr.n_inputs == 1:
    pset.addTerminal(1)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", lambda x: sr.evaluate(toolbox.compile(x)))
toolbox.register("expr_mut_leaf", gp.genFull, min_=1, max_=1)
toolbox.register("mutate_leaf", mutLeaf, expr=toolbox.expr_mut_leaf, pset=pset)
toolbox.register("expr_mut_leaf_parent", gp.genFull, min_=0, max_=0)
toolbox.register("mutate_leaf_parent", mutLeafParent, expr=toolbox.expr_mut_leaf_parent, pset=pset)
toolbox.register("mutate_local", mutLeaf, expr=toolbox.expr_mut_leaf_parent, pset=pset)


"""start sampling
"""
random.seed(1000+i)

explorer = toolbox.individual()
fit = toolbox.evaluate(explorer)[0]

with open(f"run{i}.dat", "a") as log:
    s = str(explorer).replace(" ", "")
    log.write(f"{fit} {s}\n")

rw = [deepcopy(explorer)]

count = 0
while count < max_count:

    explorer = deepcopy(rw[-1])

    # update explorer by mutation
    if explorer.height == 0:
        if random.random() < 0.5:
            explorer = toolbox.mutate_leaf(explorer)
        else:
            explorer = toolbox.mutate_local(explorer)
    elif explorer.height > max_tree_height:
        if random.random() < 0.5:
            explorer = toolbox.mutate_leaf_parent(explorer)
        else:
            explorer = toolbox.mutate_local(explorer)
    else:
        if random.random() < 1/3:
            explorer = toolbox.mutate_leaf(explorer)
        elif random.random() < 2/3:
            explorer = toolbox.mutate_leaf_parent(explorer)
        else:
            explorer = toolbox.mutate_local(explorer)

    if explorer not in rw:
        fit = toolbox.evaluate(explorer)[0]
        rw.append(deepcopy(explorer))

        with open(f"run{i}.dat", "a") as log:
            s = str(explorer).replace(" ", "")
            log.write(f"{fit} {s}\n")


    count += 1
