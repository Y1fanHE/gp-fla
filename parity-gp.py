"""Genetic Programming for Parity Problems

Created by Yifan He (heyif@outlook.com)
Last update on Feb 22, 2023
"""
import multiprocessing
import operator
import random
import sys
from deap import algorithms, base, creator,gp, tools
from benchmarks import Parity

parity = Parity(n_inputs=int(sys.argv[1]))

i = int(sys.argv[2])

with open(f"run{i}.dat", "w") as log:
    log.close()

POP_SIZE = 1000
MAX_GEN = 5000
OPT_FIT = 2**int(sys.argv[1])
CXPB, MUTPB = 0.9, 0.05

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
toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evaluate(x):
    try:
        return parity.evaluate(toolbox.compile(x))
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
