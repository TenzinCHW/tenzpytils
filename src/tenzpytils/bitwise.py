import numpy as np


def create_8bit_dset(n):
    '''Produces all values of size `n` bits as array. `n` must be an int from 1 to 8 inclusive.'''
    assert(0 < n <= 8 and type(n) == int)
    arr = np.arange(2**n).astype(np.uint8).reshape(-1, 1)
    #arr = np.array([[i] for i in range(2**n)]).astype(np.uint8)
    return np.unpackbits(arr, axis=1, bitorder='little', count=n)


def create_nbit_dset(n):
    '''Produces all values of size `n` bits as array. `n` must be an int > 0.'''
    assert(n > 0)
    r = n % 8
    nf = n // 8
    if r == 0:
        lower_bits = create_8bit_dset(8)
        nf -= 1
    else:
        lower_bits = create_8bit_dset(r)
    for _ in range(nf):
        upper_bits = np.kron(create_8bit_dset(8), np.ones((2**lower_bits.shape[1], 1), dtype=np.uint8))
        lower_bits = np.tile(lower_bits, (256, 1))
        lower_bits = np.concatenate((lower_bits, upper_bits), axis=1)
    return lower_bits


def create_ndiv2_ternary_dataset(n):
    return create_ternary_dataset(n // 2)


def create_ternary_dataset(n):
    choose_from = tuple(np.array([[0, 0], [0, 1], [1, 0]], dtype=np.uint8)[i, :] for i in range(3))
    res = np.zeros((3**n, 2*n), np.uint8)
    for i, comb in enumerate(product([0, 1, 2], repeat=n)):
        for j, c in enumerate(comb):
            res[i, 2*j:2*j+2] = choose_from[c]
    return res


def sort_bin_mat(mat):
    '''Sorts a binary matrix based on the equivalent integer value.'''
    return mat[np.lexsort([mat[:, i] for i in range(mat.shape[1])])]


def neighbours(v, n):
    '''Produces all neighbours of binary vector `v`.'''
    res = []
    for i in range(1, n+1):
        for comb in combinations(range(len(v)), i):
            for i in comb:
                neigh = np.array(v)
                neigh[i] = 1 - v[i]
            res.append(tuple(neigh))
    return res


def neighbouring_probs(states, probs, nneigh=1):
    '''Given the probabilities `probs` of each state in `states`, return array of probabilities corresponding to neighbours up to `nneigh` bit flips away.'''
    m, n = states.shape
    pm, = probs.shape
    assert(m == pm)
    state_prob_map = {tuple(states[i, :]) : probs[i] for i in range(len(probs))}
    ordered_states = sort_bin_mat(states)
    neigh_probs = np.zeros((m, sum([choose(n, i) for i in range(1, nneigh+1)])))
    for i, state in enumerate(state_prob_map.keys()):
        for j, neigh in enumerate(neighbours(state, nneigh)):
            if neigh in state_prob_map.keys():
                neigh_probs[i, j] = state_prob_map[neigh]
    return neigh_probs

