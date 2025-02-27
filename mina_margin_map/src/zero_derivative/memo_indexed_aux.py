import math

from .indexed_aux import s, si, sm, w


def si_memo(x, memo, i=0):
    if i == 0:
        return x
    elif i > 0:
        if f"s{i - 1}" in memo:
            inner = memo[f"s{i - 1}"]
        else:
            inner = si(x, memo, i - 1)
            memo[f"s{i - 1}"] = inner
        return s(inner)
    else:
        if f"s{i + 1}" in memo:
            inner = memo[f"s{i + 1}"]
        else:
            inner = si(x, memo, i + 1)
            memo[f"s{i + 1}"] = inner
        return sm(inner)


def ci_memo(x, memo, i=0):
    if f"s{i}" in memo:
        inner = memo[f"s{i}"]
    else:
        inner = si(x, i)
        memo[f"s{i}"] = inner
    return ((w(inner) + 3) ** 2) / 16


def di_memo(x, memo, i=0):
    if f"s{i}" in memo:
        inner = memo[f"s{i}"]
    else:
        inner = si(x, i)
        memo[f"s{i}"] = inner
    return ((w(inner) + 3) ** 2) / (8 * (w(inner) + 1))


def Pi_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0:
            return 1
        else:
            return wrapper(x, i - 1) + math.prod(
                [ci_memo(x, memo, j) - 1 for j in range(0, i)]
            )

    return wrapper(x, i)


def Si_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0:
            return 1
        else:
            return wrapper(x, i - 1) + math.prod(
                [di_memo(x, memo, j) - 1 for j in range(0, i)]
            )

    return wrapper(x, i)


def Qi_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0 or i == 1:
            return 0
        else:
            return wrapper(x, i - 1) + math.prod(
                [1 / (ci_memo(x, memo, -j) - 1) for j in range(1, i)]
            )

    return wrapper(x, i)


def Ti_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0 or i == 1:
            return 0
        else:
            return wrapper(x, i - 1) + math.prod(
                [1 / (di_memo(x, memo, -j) - 1) for j in range(1, i)]
            )

    return wrapper(x, i)
