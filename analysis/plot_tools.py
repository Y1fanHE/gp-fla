from zipfile import ZipFile
import pandas as pd
import igraph
import networkx as nx
import numpy as np

def get_graph(
    zfname,
    threshold,
    global_fitness,
    direction=1,
    vertex_size_init=5,
    vertex_size_step=.3,
    edge_width_init=1,
    edge_width_step=.01,
    vertex_color_normal="lightgray",
    vertex_color_global="green",
    edge_color_inc="red",
    edge_color_dec="blue",
    monotonic=False,
    strict=False
):
    zf = ZipFile(zfname)

    df = pd.concat(
        [pd.read_csv(zf.open(i), header=None, delimiter=" ") for i in zf.namelist()],
        ignore_index=True
    )
    df.columns = ["f1", "n1", "f2", "n2", "mu"]
    df = df[direction*df.f2>=direction*threshold]
    if monotonic and strict:
        df = df[direction*df.f2>direction*df.f1]
    if monotonic and not strict:
        df = df[direction*df.f2>=direction*df.f1]

    tmp1 = df[["f1","n1"]]
    tmp2 = df[["f2","n2"]]
    tmp1.columns = ["f", "n"]
    tmp2.columns = ["f", "n"]
    df_trans = pd.concat([tmp1, tmp2])
    df_trans_drop = df_trans.drop_duplicates()

    nodes = list(df_trans_drop.n)
    fits = list(df_trans_drop.f)
    
    df_drop = df[["n1","n2","mu"]].drop_duplicates()
    edges = [list(e) for e in df_drop[["n1","n2"]].values]
    mus = list(df_drop.mu)

    node_visit_counts = [0]*len(nodes)
    for n in df_trans.n:
        idx = nodes.index(n)
        node_visit_counts[idx] += 1

    edge_counts = [0]*len(edges)
    for e in df[["n1","n2"]].values:
        idx = edges.index(list(e))
        edge_counts[idx] += 1
    
    g = igraph.Graph(directed=True)
    g.add_vertices(nodes)
    g.add_edges(edges)
    
    g.vs["fit"] = fits
    g.vs["size"] = [vertex_size_init+vertex_size_step*i for i in node_visit_counts]
    g.vs["color"] = [vertex_color_normal if fit*direction<global_fitness*direction else vertex_color_global for fit in fits]
    g.es["width"] = [edge_width_init+edge_width_step*i for i in edge_counts]
    g.es["color"] = [edge_color_inc if m=="leaf" else edge_color_dec for m in mus]

    return g


def get_networkx_plot_var(
    zfname,
    threshold,
    global_fitness,
    direction=1,
    vertex_size_init=3,
    vertex_size_step=.3,
    edge_width_init=1,
    edge_width_step=.01,
    vertex_color_normal="#d3d3d3",
    vertex_color_global="#00ff00",
    edge_color_inc="#ff0000",
    edge_color_dec="#0000ff",
    monotonic=False,
    log_scale=False,
    strict=False
):
    g = get_graph(
        zfname,
        threshold,
        global_fitness,
        direction,
        vertex_size_init,
        vertex_size_step,
        edge_width_init,
        edge_width_step,
        vertex_color_normal,
        vertex_color_global,
        edge_color_inc,
        edge_color_dec,
        monotonic=monotonic,
        strict=strict
    ).to_networkx()
    pos = nx.spring_layout(g, dim=3)

    vertex_size = []
    vertex_color = []
    vertex_xyz = []
    for v in pos:
        if not log_scale:
            pos[v][-1] = g.nodes()[v].get("fit")
        else:
            pos[v][-1] = np.log(g.nodes()[v].get("fit")+threshold)
        vertex_xyz.append(pos[v])
        vertex_size.append( 15+1*(g.nodes()[v].get("size")-vertex_size_init)/vertex_size_step )
        vertex_color.append(g.nodes()[v].get("color"))
    vertex_xyz = np.array(vertex_xyz)
    edge_xyz = []
    edge_width = []
    edge_color = []
    for u, v in g.edges():
        edge_xyz.append((pos[u], pos[v]))
        edge_width.append( 1+.005*(g.edges()[(u,v)].get("width")-edge_width_init)/edge_width_step )
        edge_color.append(g.edges()[(u,v)].get("color"))
    edge_xyz = np.array(edge_xyz)

    return vertex_xyz, edge_xyz, vertex_size, edge_width, vertex_color, edge_color

def set_ax(ax):
    ax.view_init(5, 150)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor("black")
    ax.yaxis.pane.set_edgecolor("black")
    ax.zaxis.pane.set_edgecolor("black")
    ax.xaxis.pane.set_facecolor("none")
    ax.yaxis.pane.set_facecolor("none")
    ax.zaxis.pane.set_facecolor("none")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

def get_evo_curve(zfname, max_gen=5000):
    zf = ZipFile(zfname)

    g_lst = []
    for i in zf.namelist():
        g = len(np.loadtxt(zf.open(i), delimiter=","))
        g_lst.append(g)
        
    r_lst = []
    for i in range(max_gen):
        r_lst.append(np.array(g_lst) <= i)
        
    return np.array(r_lst).mean(axis=1)