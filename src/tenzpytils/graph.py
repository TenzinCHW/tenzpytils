import numpy as np

def ind(i, j, V):
    """ returns index into (1D) internal array edges of V(V-1)/2 binary vector """
    if i < j:
        return (i * V - i*(i+1) // 2 + j - i - 1)
    return (j * V - j * (j + 1) // 2 + i - j - 1)

def sample_clique(V, K):
    """ produce a random K-clique on an V-node graph """
    edges = np.zeros(V * (V-1) // 2, dtype=int)
    clique_array = np.random.permutation(V)[0:K]  # clique vertices
    for i in clique_array:
        for j in clique_array:
            if i != j:
                edges[ind(i, j, V)] = 1
    return edges

def sample_bipartite(V, K, adjacency_matrix=False):
    # left vertices
    left_verts = np.random.permutation(V)[0:K]
    bipart = np.zeros((V, V))
    edges = np.zeros(V * (V-1) // 2, dtype=int)
    for i in left_verts:
        for j in range(V):
            if j not in left_verts:
                bipart[i, j] = 1; bipart[j, i] = 1
                edges[ind(i, j, V)] = 1
    if adjacency_matrix:
        return bipart
    return edges

def exact_match(a, b):
    return np.all(a == b)

def isunique(sample, collection):
    return all([not exact_match(sample, c) for c in collection])

def sample_n_unique_cliques(V, K, n):
    cliques = []
    while len(cliques) < n:
        a = sample_clique(V, K)
        if isunique(a, cliques):
            cliques.append(a)
    return np.array(cliques)

def sample_n_cliques(V, K, n):
    return np.array([sample_clique(V, K) for _ in range(n)])

def noise_edges(graph, p):
    '''Assumes that graph is a vectorised adjacency matrix and 0 < p < 1 is the probability that an edge is flipped.'''
    g = graph.copy()
    graph_sz = len(graph)
    randvals = np.random.rand(graph_sz)
    for s, i in zip(randvals, range(graph_sz)):
        if s < p:
            g[i] = 1 - graph[i]
    return g

