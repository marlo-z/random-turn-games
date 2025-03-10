import math

from .aux import s, sm, w


def si(x, i=0):
    if i == 0:
        return x
    elif i > 0:
        inner = si(x, i - 1)
        return s(inner)
    else:
        inner = si(x, i + 1)
        return sm(inner)


def ci(x, i=0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / 16


def di(x, i=0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / (8 * (w(inner) + 1))


def Pi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Pi(x, i - 1) + math.prod([ci(x, j) - 1 for j in range(0, i)])


def Si(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Si(x, i - 1) + math.prod([di(x, j) - 1 for j in range(0, i)])


def Qi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Qi(x, i - 1) + math.prod([1 / (ci(x, -j) - 1) for j in range(1, i)])


def Ti(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Ti(x, i - 1) + math.prod([1 / (di(x, -j) - 1) for j in range(1, i)])
