from zipfile import ZipFile
import pandas as pd
import re
import multiprocessing
from functools import partial
from zss import Node, simple_distance

def get_fitness_distance(zfname, arity, direction=1, global_optima_tree=None, global_optima_fit=None):
    with open(zfname.replace(".zip", "-fdc.csv"), "w") as csv:
        csv.close()
    zf = ZipFile(zfname)
    df = pd.concat(
        [pd.read_csv(zf.open(i), header=None, delimiter=" ") for i in zf.namelist()],
        ignore_index=True
    )
    df.columns = ["f1", "n1", "f2", "n2", "mu"]
    tmp1 = df[["f1","n1"]]
    tmp2 = df[["f2","n2"]]
    tmp1.columns = ["f", "n"]
    tmp2.columns = ["f", "n"]
    df_trans = pd.concat([tmp1, tmp2]).drop_duplicates()
    df_trans_val = df_trans.values

    if not global_optima_tree:
        if direction == 1:
            global_optimas = df_trans[df_trans.f==df_trans.f.max()]
        if direction == -1:
            global_optimas = df_trans[df_trans.f==df_trans.f.min()]
        global_optima_fit = global_optimas.f.values[0]
        lengths = []
        for i in global_optimas.n:
            expr_ = []
            for item in re.split("[ \t\n\r\f\v(),]", i):
                if item != "":
                    expr_.append(item)
            lengths.append(len(expr_))
        idx = lengths.index(max(lengths))
        global_optima_tree = expr2tree(global_optimas.n.values[idx], arity)
    else:
        global_optima_tree = expr2tree(global_optima_tree, arity)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(
        partial(write_in_parallel,
                zfname=zfname,
                df_trans_val=df_trans_val,
                arity=arity,
                global_optima_tree=global_optima_tree,
                global_optima_fit=global_optima_fit),
        list(range(len(df_trans)))
    )
    pool.close()


def write_in_parallel(i, zfname, df_trans_val, arity, global_optima_tree, global_optima_fit):
    with open(zfname.replace(".zip", "-fdc.csv"), "a") as csv:
        f, n = list(df_trans_val[i])
        tree = expr2tree(n, arity)
        d = simple_distance(tree, global_optima_tree)
        f = abs(global_optima_fit - f)
        csv.write(f"{f},{d}\n")
        return 0


def expr2tree(expr, arity):
    expr_ = []
    for item in re.split("[ \t\n\r\f\v(),]", expr):
        if item != "":
            expr_.append(item)
    nodes = list(range(len(expr_)))
    edges = list()
    labels = dict()
    stack = []
    for i, node in enumerate(expr_):
        if stack:
            edges.append((stack[-1][0], i))
            stack[-1][1] -= 1
        labels[i] = node
        stack.append([i, arity[node]])
        while stack and stack[-1][1] == 0:
            stack.pop()
    tree = dict()
    if len(nodes) == 1:
        return Node(labels[0])
    for n1, n2 in edges:
        if n1 not in tree:
            tree[n1] = Node(labels[n1])
        if n2 not in tree:
            tree[n2] = Node(labels[n2])
        tree[n1].addkid(tree[n2])
    return tree[0]
