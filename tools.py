"""Local Search and Mutation Methods of Sampling Algorithm

Created by Yifan He (heyif@outlook.com)
Last update on Feb 20, 2023
"""
import random
from copy import deepcopy
from deap import gp
from inspect import isclass
from itertools import product


def mutLocal(individual, pset):
    individual_ = deepcopy(individual)
    individuals = []
    for index in range(len(individual_)):
        slice_ = individual_.searchSubtree(index)
        type_ = individual_[index].ret
        if gp.PrimitiveTree(individual_[slice_]).height == 0:
            for term in pset.terminals[type_]:
                if isclass(term):
                    term = term()
                ind_ = deepcopy(individual_)
                ind_[slice_] = [term]
                if ind_ != individual:
                    individuals.append(ind_)
    return individuals


def mutLeaf(individual, expr, pset):
    individual_ = deepcopy(individual)
    while True:
        index = random.randrange(0,len(individual_))
        slice_ = individual_.searchSubtree(index)
        type_ = individual_[index].ret
        if gp.PrimitiveTree(individual_[slice_]).height == 0:
            break
    individual_[slice_] = expr(pset=pset, type_=type_)
    return individual_


def mutLeafParent(individual, expr, pset):
    individual_ = deepcopy(individual)
    while True:
        index = random.randrange(0,len(individual_))
        slice_ = individual_.searchSubtree(index)
        type_ = individual_[index].ret
        if gp.PrimitiveTree(individual_[slice_]).height == 1:
            break
    individual_[slice_] = expr(pset=pset, type_=type_)
    return individual_


def tree1(pset):
    expr_lst = []
    for root in pset.primitives[object]:
        for child in product(pset.terminals[object], repeat=root.arity):
            expr = [root]
            expr.extend(list(child))
            expr_lst.append(expr)
    return expr_lst


def mutNeighbor(individual, tset, pset):
    individual_ = deepcopy(individual)
    individuals = []
    for index in range(len(individual_)):
        slice_ = individual_.searchSubtree(index)
        type_ = individual_[index].ret
        # mutate if a node is leaf
        if gp.PrimitiveTree(individual_[slice_]).height == 0:

            # change node into another terminal
            for term in pset.terminals[type_]:
                if isclass(term):
                    term = term()
                ind_ = deepcopy(individual_)
                ind_[slice_] = [term]
                if ind_ != individual:
                    individuals.append(ind_)

            # change node into a tree with height of 1
            for t in tset:
                ind_ = deepcopy(individual_)
                ind_[slice_] = t
                individuals.append(ind_)

        # mutate if a node is the parent of leaf
        if gp.PrimitiveTree(individual_[slice_]).height == 1:

            # change node into another terminal
            for term in pset.terminals[type_]:
                if isclass(term):
                    term = term()
                ind_ = deepcopy(individual_)
                ind_[slice_] = [term]
                if ind_ != individual:
                    individuals.append(ind_)

    random.shuffle(individuals)

    return individuals