"""Random Walk for Parity Problems

Created by Yifan He (heyif@outlook.com)
Last update on Mar 02, 2023
"""
import operator
import random
import sys
from copy import deepcopy
from deap import base, creator,gp, tools
from benchmarks import Parity
from tools import mutLeaf, mutLeafParent

parity = Parity(n_inputs=int(sys.argv[1]))

i = int(sys.argv[2])
max_count = int(sys.argv[3])
max_tree_height = int(sys.argv[4])

with open(f"run{i}.dat", "w") as log:
    log.close()

pset = gp.PrimitiveSet("MAIN", parity.n_inputs, "IN")
pset.addPrimitive(operator.and_, 2, "AND")
pset.addPrimitive(operator.or_,  2, "OR")
pset.addPrimitive(operator.xor,  2, "XOR")
pset.addPrimitive(operator.not_, 1, "NOT")
pset.addTerminal(1)
pset.addTerminal(0)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", lambda x: parity.evaluate(toolbox.compile(x)))
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
