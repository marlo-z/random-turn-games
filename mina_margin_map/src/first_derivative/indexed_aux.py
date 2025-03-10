import numpy as np

from ..zero_derivative import ci, di
from .aux import cp, dp, si, smp, sp


def spi(x, i=0):
    if i == 0:
        return 1
    elif i > 0:
        return sp(si(x, i - 1)) * spi(x, i - 1)
    else:
        return smp(si(x, i + 1)) * spi(x, i + 1)


def cpi(x, i=0):
    return cp(si(x, i)) * spi(x, i)


def dpi(x, i=0):
    return dp(si(x, i)) * spi(x, i)


def Ai(x, i=0):
    return np.prod([di(x, n) - 1 for n in range(0, i + 1)])


def Bi(x, i=0):
    return np.prod([ci(x, n) - 1 for n in range(0, i + 1)])


def Ci(x, i=0):
    return np.prod([1 / (di(x, -n) - 1) for n in range(1, i + 1)])


def Di(x, i=0):
    return np.prod([1 / (ci(x, -n) - 1) for n in range(1, i + 1)])


def Ei(x, i=0):
    return sum([dpi(x, j) / (di(x, j) - 1) for j in range(0, i + 1)])


def Fi(x, i=0):
    return sum([cpi(x, j) / (ci(x, j) - 1) for j in range(0, i + 1)])


def Gi(x, i=0):
    return sum([-dpi(x, -j) / (di(x, -j) - 1) for j in range(1, i + 1)])


def Hi(x, i=0):
    return sum([-cpi(x, -j) / (ci(x, -j) - 1) for j in range(1, i + 1)])
