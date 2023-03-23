"""Genetic Programming with MAP-Elites for Parity Problems

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

best_fitness = 0
fitnesses = list(pool.map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    best_fitness = max(best_fitness, fit[0])

    ind.fitness.values = fit
    map_id = (",".join([i.name for i in ind[:2]]), ind.height)
    elite = map_elites.get(map_id)
    if elite:
        if elite.fitness.values[0] < fit[0]:
            map_elites.update({map_id: toolbox.clone(ind)})
    else:
        map_elites.update({map_id: ind})

g = 0
while best_fitness < OPT_FIT and g < MAX_GEN:
    g = g + 1

    offspring = toolbox.select(list(map_elites.values()), len(pop))
    offspring = list(map(toolbox.clone, offspring))

    offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPB)

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(pool.map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        best_fitness = max(best_fitness, fit[0])

        ind.fitness.values = fit
        map_id = (",".join([i.name for i in ind[:2]]), ind.height)
        elite = map_elites.get(map_id)
        if elite:
            if elite.fitness.values[0] < fit[0]:
                map_elites.update({map_id: toolbox.clone(ind)})
        else:
            map_elites.update({map_id: toolbox.clone(ind)})

    with open(f"run{i}.dat", "a") as log:
        log.write(f"{g},{best_fitness}\n")

pool.close()
