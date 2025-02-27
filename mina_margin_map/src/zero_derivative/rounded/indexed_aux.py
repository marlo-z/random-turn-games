import math

from ...utils import round_down, round_up
from .aux import downs, downsm, downw, ups, upsm, upw


def upsi(x, i=0):
    if i == 0:
        return round_up(x)
    elif i > 0:
        inner = upsi(x, i - 1)
        return ups(inner)
    else:
        inner = upsi(x, i + 1)
        return upsm(inner)


def downsi(x, i=0):
    if i == 0:
        return round_down(x)
    elif i > 0:
        inner = downsi(x, i - 1)
        return downs(inner)
    else:
        inner = downsi(x, i + 1)
        return downsm(inner)


def upci(x, i=0):
    inner = upsi(x, i)
    return round_up(((upw(inner) + 3) ** 2) / 16)


def downci(x, i=0):
    inner = downsi(x, i)
    return round_down(((downw(inner) + 3) ** 2) / 16)


def updi(x, i=0):
    innerup = upsi(x, i)
    innerdown = downsi(x, i)
    return round_up(((upw(innerup) + 3) ** 2) / (8 * (downw(innerdown) + 1)))


def downdi(x, i=0):
    innerup = upsi(x, i)
    innerdown = downsi(x, i)
    return round_down(((downw(innerdown) + 3) ** 2) / (8 * (upw(innerup) + 1)))


def upPi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return upPi(x, i - 1) + round_up(
            math.prod([upci(x, j) - 1 for j in range(0, i)])
        )


def downPi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return downPi(x, i - 1) + round_down(
            math.prod([downci(x, j) - 1 for j in range(0, i)])
        )


def upSi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return upSi(x, i - 1) + round_up(
            math.prod([updi(x, j) - 1 for j in range(0, i)])
        )


def downSi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return downSi(x, i - 1) + round_down(
            math.prod([downdi(x, j) - 1 for j in range(0, i)])
        )


def upQi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return upQi(x, i - 1) + round_up(
            math.prod([1 / (downci(x, -j) - 1) for j in range(1, i)])
        )


def downQi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return downQi(x, i - 1) + round_down(
            math.prod([1 / (upci(x, -j) - 1) for j in range(1, i)])
        )


def upTi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return upTi(x, i - 1) + round_up(
            math.prod([1 / (downdi(x, -j) - 1) for j in range(1, i)])
        )


def downTi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return downTi(x, i - 1) + round_down(
            math.prod([1 / (updi(x, -j) - 1) for j in range(1, i)])
        )
