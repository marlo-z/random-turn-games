from ..zero_derivative import sm, w


def wp(x):
    return 4 / ((8 * x + 1) ** (1 / 2))


def sp(x):
    return wp(x) * (w(x) - 1) * (w(x) + 15) / (4 * (w(x) + 7) ** 2)


def smp(x):
    return sp(1 / x) * sm(x) ** 2 / x**2


def cp(x):
    return wp(x) * (w(x) + 3) / 8


def dp(x):
    return wp(x) * (w(x) + 3) * (w(x) - 1) / (8 * (w(x) + 1) ** 2)
