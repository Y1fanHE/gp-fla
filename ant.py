"""Local Optima Networks for Artificial Ant Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 20, 2023
"""
import random
import sys
from copy import deepcopy
from functools import partial
from deap import base, creator, tools, gp
from benchmarks import AntSimulator
from tools import mutLocal, mutLeaf, mutLeafParent


max_steps = {
    "1": 600,
    "2": 800
}

map_files = {
    "1": "santafe_trail",
    "2": "losaltos_trail"
}

max_step = max_steps[sys.argv[1]]
map_file = map_files[sys.argv[1]]

ant = AntSimulator(max_step)
with open(f"ant/{map_file}.txt") as trail_file:
    ant.parse_matrix(trail_file)

i = int(sys.argv[2])
max_count = int(sys.argv[3])
max_tree_height = int(sys.argv[4])

with open(f"run{i}.dat", "w") as log:
    log.close()

def progn(*args):
    for arg in args:
        arg()

def prog2(out1, out2): 
    return partial(progn,out1,out2)

def prog3(out1, out2, out3):
    return partial(progn,out1,out2,out3)


pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(ant.if_food_ahead, 2, "S")
pset.addPrimitive(prog2, 2, "P2")
pset.addPrimitive(prog3, 3, "P3")
pset.addTerminal(ant.move_forward, "F")
pset.addTerminal(ant.turn_left, "L")
pset.addTerminal(ant.turn_right, "R")

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)

def evalArtificialAnt(individual):
    # Transform the tree expression to functional Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    ant.run(routine)
    return ant.eaten,

toolbox.register("evaluate", evalArtificialAnt)
toolbox.register("select", tools.selTournament, tournsize=7)
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

print(f"finished ant-run{i} with best fitness {blo.fitness.values[0]}")
