def kl_div(p1, p2):
    p2p = p2 + 1e-10
    p2p /= p2p.sum()
    p1p = p1 + 1e-10
    p1p /= p1p.sum()
    return (p1 * np.log(p1p/p2p)).sum()

