import numpy as np

from ...utils import round_down, round_up
from ...zero_derivative.rounded import downci, downdi, downsi, upci, updi
from .aux import downcp, downdp, downsmp, downsp, upcp, updp, upsi, upsmp, upsp


def upspi(x, i=0):
    if i == 0:
        return 1
    elif i > 0:
        return upsp(upsi(x, i - 1)) * upspi(x, i - 1)
    else:
        return upsmp(upsi(x, i + 1)) * upspi(x, i + 1)


def downspi(x, i=0):
    if i == 0:
        return 1
    elif i > 0:
        return downsp(downsi(x, i - 1)) * downspi(x, i - 1)
    else:
        return downsmp(downsi(x, i + 1)) * downspi(x, i + 1)


def upcpi(x, i=0):
    return upcp(upsi(x, i)) * upspi(x, i)


def downcpi(x, i=0):
    return downcp(downsi(x, i)) * downspi(x, i)


def updpi(x, i=0):
    return updp(upsi(x, i)) * upspi(x, i)


def downdpi(x, i=0):
    return downdp(downsi(x, i)) * downspi(x, i)


def upAi(x, i=0):
    return round_up(np.prod([updi(x, n) - 1 for n in range(0, i + 1)]))


def downAi(x, i=0):
    return round_down(np.prod([downdi(x, n) - 1 for n in range(0, i + 1)]))


def upBi(x, i=0):
    return round_up(np.prod([upci(x, n) - 1 for n in range(0, i + 1)]))


def downBi(x, i=0):
    return round_down(np.prod([downci(x, n) - 1 for n in range(0, i + 1)]))


def upCi(x, i=0):
    return round_up(np.prod([1 / (downdi(x, -n) - 1) for n in range(1, i + 1)]))


def downCi(x, i=0):
    return round_down(np.prod([1 / (updi(x, -n) - 1) for n in range(1, i + 1)]))


def upDi(x, i=0):
    return round_up(np.prod([1 / (downci(x, -n) - 1) for n in range(1, i + 1)]))


def downDi(x, i=0):
    return round_down(np.prod([1 / (upci(x, -n) - 1) for n in range(1, i + 1)]))


def upEi(x, i=0):
    return round_up(sum([updpi(x, j) / (downdi(x, j) - 1) for j in range(0, i + 1)]))


def downEi(x, i=0):
    return round_down(sum([downdpi(x, j) / (updi(x, j) - 1) for j in range(0, i + 1)]))


def upFi(x, i=0):
    return round_up(sum([upcpi(x, j) / (downci(x, j) - 1) for j in range(0, i + 1)]))


def downFi(x, i=0):
    return round_down(sum([downcpi(x, j) / (upci(x, j) - 1) for j in range(0, i + 1)]))


def upGi(x, i=0):
    return round_up(
        sum([-downdpi(x, -j) / (downdi(x, -j) - 1) for j in range(1, i + 1)])
    )


def downGi(x, i=0):
    return round_down(sum([-updpi(x, -j) / (updi(x, -j) - 1) for j in range(1, i + 1)]))


def upHi(x, i=0):
    return round_up(
        sum([-downcpi(x, -j) / (downci(x, -j) - 1) for j in range(1, i + 1)])
    )


def downHi(x, i=0):
    return round_down(sum([-upcpi(x, -j) / (upci(x, -j) - 1) for j in range(1, i + 1)]))
