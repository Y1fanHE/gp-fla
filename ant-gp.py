"""Local Optima Networks for Artificial Ant Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 20, 2023
"""
import multiprocessing
import operator
import math
import random
import sys
from functools import partial
from deap import algorithms, base, creator, tools, gp
from benchmarks import AntSimulator


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

POP_SIZE = 1000
MAX_GEN = 5000
OPT_FIT = 89 if sys.argv[1]=="1" else 157
CXPB, MUTPB = 0.9, 0.05

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
toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evaluate(individual):
    try:
        # Transform the tree expression to functional Python code
        routine = gp.compile(individual, pset)
        # Run the generated routine
        ant.run(routine)
        return ant.eaten,
    except Exception:
        return -1,

toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))

"""start running
"""
random.seed(1000+i)
pool = multiprocessing.Pool(multiprocessing.cpu_count())

pop = toolbox.population(n=POP_SIZE)

fitnesses = list(pool.map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
fits = [ind.fitness.values[0] for ind in pop]

g = 0
while max(fits) < OPT_FIT and g < MAX_GEN:
    g = g + 1

    offspring = toolbox.select(pop, len(pop))
    offspring = list(map(toolbox.clone, offspring))

    offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPB)

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(pool.map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    pop[:] = offspring
    fits = [ind.fitness.values[0] for ind in pop]
    
    with open(f"run{i}.dat", "a") as log:
        log.write(f"{g},{max(fits)}\n")

pool.close()
