def w(x):
    return (8 * x + 1) ** (1 / 2)


def s(x):
    return ((w(x) - 1) ** 2) / (4 * (w(x) + 7))


def sm(x):
    return 1 / s(1 / x)
