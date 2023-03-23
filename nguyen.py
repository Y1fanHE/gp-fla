"""Local Optima Networks for Symbolic Regression Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 24, 2023
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
toolbox.register("local", mutLocal, pset=pset)

"""start sampling
"""
random.seed(1000+i)

# initialize explorer randomly
explorer = toolbox.individual()
fit = toolbox.evaluate(explorer)
explorer.fitness.values = fit

# improve explorer by local search
lo = deepcopy(explorer)
while True:
    neighbors = mutLocal(explorer, pset) # neighbors
    improved = False
    for n in neighbors:
        fit_ = toolbox.evaluate(n)
        if fit_[0] < explorer.fitness.values[0]:
            explorer = n
            explorer.fitness.values = fit_
            improved = True
    if not improved:
        break

# set best local optima
blo = deepcopy(lo)

count = 0
while count < max_count:

    # exploring from best local optima
    explorer = deepcopy(blo)

    # update explorer by mutation
    if explorer.height == 0:
        explorer = toolbox.mutate_leaf(explorer)
        mutation_type = "leaf"
    elif explorer.height > max_tree_height:
        explorer = toolbox.mutate_leaf_parent(explorer)
        mutation_type = "leaf_parent"
    else:
        if random.random() < 0.5:
            explorer = toolbox.mutate_leaf(explorer)
            mutation_type = "leaf"
        else:
            explorer = toolbox.mutate_leaf_parent(explorer)
            mutation_type = "leaf_parent"
    fit = toolbox.evaluate(explorer)
    explorer.fitness.values = fit

    # improve explorer by local search
    lo = deepcopy(explorer)
    while True:
        neighbors = mutLocal(explorer, pset) # neighbors
        improved = False
        for n in neighbors:
            fit_ = toolbox.evaluate(n)
            if fit_[0] < explorer.fitness.values[0]:
                explorer = n
                explorer.fitness.values = fit_
                improved = True
        if not improved:
            break

    if True:
        if str(lo) != str(blo):
            # record escape edge: blo->lo
            with open(f"run{i}.dat", "a") as log:
                s = str(blo.fitness.values[0]) + " "
                s += str(blo).replace(" ","") + " "
                s += str(lo.fitness.values[0]) + " "
                s += str(lo).replace(" ","") + " "
                s += mutation_type + "\n"
                log.write(s)

    # if new local optima is better than best local optima
    if lo.fitness.values[0] <= blo.fitness.values[0]:

        # update best local optima
        blo = deepcopy(lo)

    count += 1

print(f"finished sr-run{i} with best fitness {blo.fitness.values[0]}")
