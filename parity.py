"""Local Optima Networks for Parity Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 20, 2023
"""
import operator
import random
import sys
from copy import deepcopy
from deap import base, creator,gp, tools
from benchmarks import Parity
from tools import mutLocal, mutLeaf, mutLeafParent

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
        if fit_[0] > explorer.fitness.values[0]:
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
            if fit_[0] > explorer.fitness.values[0]:
                explorer = n
                explorer.fitness.values = fit_
                improved = True
        if not improved:
            break

    if True:
        if str(lo) != str(blo):
            # record escape edge: blo->lo
            with open(f"run{i}.dat", "a") as log:
                s = str(int(blo.fitness.values[0])) + " "
                s += str(blo).replace(" ","") + " "
                s += str(int(lo.fitness.values[0])) + " "
                s += str(lo).replace(" ","") + " "
                s += mutation_type + "\n"
                log.write(s)

    # if new local optima is better than best local optima
    if lo.fitness.values[0] >= blo.fitness.values[0]:

        # update best local optima
        blo = deepcopy(lo)

    count += 1

print(f"finished parity-run{i} with best fitness {blo.fitness.values[0]}")
