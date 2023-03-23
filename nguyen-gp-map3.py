"""Genetic Programming with MAP-Elites for Symbolic Regression Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 24, 2023
"""
import multiprocessing
import operator
import math
import random
import sys
from deap import algorithms, base, creator, gp, tools
from benchmarks import SymbolicRegression


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

with open(f"run{i}.dat", "w") as log:
    log.close()

POP_SIZE = 1000
MAX_GEN = 5000
OPT_FIT = 1e-05
CXPB, MUTPB = 0.9, 0.05

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
toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evaluate(x):
    try:
        return sr.evaluate(toolbox.compile(x))
    except Exception:
        return math.inf,

toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selRandom)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=5)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=15))


"""start running
"""
random.seed(1000+i)
pool = multiprocessing.Pool(multiprocessing.cpu_count())

map_elites = dict()
pop = toolbox.population(n=POP_SIZE)

best_fitness = math.inf
fitnesses = list(pool.map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    best_fitness = min(best_fitness, fit[0])

    ind.fitness.values = fit
    map_id = (",".join([i.name for i in ind[-2:]]), ind.height)
    elite = map_elites.get(map_id)
    if elite:
        if elite.fitness.values[0] > fit[0]:
            map_elites.update({map_id: toolbox.clone(ind)})
    else:
        map_elites.update({map_id: ind})

g = 0
while best_fitness > OPT_FIT and g < MAX_GEN:
    g = g + 1

    offspring = toolbox.select(list(map_elites.values()), len(pop))
    offspring = list(map(toolbox.clone, offspring))

    offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPB)

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(pool.map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        best_fitness = min(best_fitness, fit[0])

        ind.fitness.values = fit
        map_id = (",".join([i.name for i in ind[-2:]]), ind.height)
        elite = map_elites.get(map_id)
        if elite:
            if elite.fitness.values[0] > fit[0]:
                map_elites.update({map_id: toolbox.clone(ind)})
        else:
            map_elites.update({map_id: toolbox.clone(ind)})

    with open(f"run{i}.dat", "a") as log:
        log.write(f"{g},{best_fitness}\n")

pool.close()
