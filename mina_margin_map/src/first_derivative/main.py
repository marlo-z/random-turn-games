from utils import round_down, round_up

from ..zero_derivative import Pi, Qi, Si, Ti, ci, di
from ..zero_derivative.main import M, calculate_bounds, calculate_rounded_bounds
from ..zero_derivative.rounded import (
    downPi,
    downQi,
    downSi,
    downTi,
    upPi,
    upQi,
    upSi,
    upTi,
)
from .indexed_aux import Ai, Bi, Ci, Di, Ei, Fi, Gi, Hi, cpi, dpi
from .rounded import (
    downAi,
    downBi,
    downCi,
    downDi,
    downEi,
    downFi,
    downGi,
    downHi,
    upAi,
    upBi,
    upCi,
    upDi,
    upEi,
    upFi,
    upGi,
    upHi,
)

# TODO: deal with floating point


def block2_upper(l, k, x, mesh):
    return (
        sum([Ei(x, i) * Ai(x + mesh, i) for i in range(k)])
        + sum([Gi(x + mesh, i) * Ci(x, i) for i in range(1, l - 1)])
    ) / (Si(x, k) + Ti(x + mesh, l))


def block2_upper_rounded(l, k, x, mesh):
    return round_up(
        round_up(sum([upEi(x, i) * upAi(x + mesh, i) for i in range(k)]))
        + round_up(sum([upGi(x + mesh, i) * upCi(x, i) for i in range(1, l - 1)]))
    ) / round_down(downSi(x, k) + downTi(x + mesh, l))


def block2_lower(l, k, x, mesh):
    return (
        sum([Ei(x + mesh, i) * Ai(x, i) for i in range(k)])
        + sum([Gi(x, i) * Ci(x + mesh, i) for i in range(1, l - 1)])
    ) / (Si(x + mesh, k) + Ti(x, l))


def block2_lower_rounded(l, k, x, mesh):
    return round_down(
        round_down(sum([downEi(x + mesh, i) * downAi(x, i) for i in range(k)]))
        + round_down(sum([downGi(x, i) * downCi(x + mesh, i) for i in range(1, l - 1)]))
    ) / round_up(upSi(x + mesh, k) + upTi(x, l))


def block2(l, k, x):
    return (
        sum([Ei(x, i) * Ai(x, i) for i in range(k)])
        + sum([Gi(x, i) * Ci(x, i) for i in range(1, l - 1)])
    ) / (Si(x, k) + Ti(x, l))


def block3_upper(l, k, x, mesh):
    return (
        sum([Fi(x, i) * Bi(x + mesh, i) for i in range(k)])
        + sum([Hi(x + mesh, i) * Di(x, i) for i in range(1, l - 1)])
    ) / (Pi(x, k) + Qi(x + mesh, l))


def block3_upper_rounded(l, k, x, mesh):
    return round_up(
        round_up(sum([upFi(x, i) * upBi(x + mesh, i) for i in range(k)]))
        + round_up(sum([upHi(x + mesh, i) * upDi(x, i) for i in range(1, l - 1)]))
    ) / round_down(downPi(x, k) + downQi(x + mesh, l))


def block3_lower(l, k, x, mesh):
    return (
        sum([Fi(x + mesh, i) * Bi(x, i) for i in range(k)])
        + sum([Hi(x, i) * Di(x + mesh, i) for i in range(1, l - 1)])
    ) / (Pi(x + mesh, k) + Qi(x, l))


def block3_lower_rounded(l, k, x, mesh):
    return round_down(
        round_down(sum([downFi(x + mesh, i) * downBi(x, i) for i in range(k)]))
        + round_down(sum([downHi(x, i) * downDi(x + mesh, i) for i in range(1, l - 1)]))
    ) / round_up(upPi(x + mesh, k) + upQi(x, l))


def block3(l, k, x):
    return (
        sum([Fi(x, i) * Bi(x, i) for i in range(k)])
        + sum([Hi(x, i) * Di(x, i) for i in range(1, l - 1)])
    ) / (Pi(x, k) + Qi(x, l))


def Mp(l, k, x):
    b1 = 1 / x
    b2 = block2(l, k, x)
    b3 = block3(l, k, x)

    return (b1 + b2 - b3) * M(l, k, x)


def calculate_derivative_bounds(l, k, x, mesh):
    b1_upper = 1 / x
    b1_lower = 1 / (x + mesh)

    b2_upper = block2_upper(l, k, x, mesh)
    b2_lower = block2_lower(l, k, x, mesh)

    b3_upper = block3_upper(l, k, x, mesh)
    b3_lower = block3_lower(l, k, x, mesh)

    M54_upper, M54_lower = calculate_bounds(l, k, x, mesh)

    upper = (b1_upper + b2_upper - b3_lower) * M54_upper
    lower = (b1_lower + b2_lower - b3_upper) * M54_lower

    return upper, lower


def calculate_derivative_bounds_rounded(l, k, x, mesh):
    b1_upper = round_up(1 / x)
    b1_lower = round_down(1 / (x + mesh))

    b2_upper = block2_upper_rounded(l, k, x, mesh)
    b2_lower = block2_lower_rounded(l, k, x, mesh)

    b3_upper = block3_upper_rounded(l, k, x, mesh)
    b3_lower = block3_lower_rounded(l, k, x, mesh)

    M54_upper, M54_lower = calculate_rounded_bounds(l, k, x, mesh)

    upper = round_up((b1_upper + b2_upper - b3_lower) * M54_upper)
    lower = round_down((b1_lower + b2_lower - b3_upper) * M54_lower)

    return upper, lower


"""M21 derivative"""


def M21p(x):
    block1 = 1 / x
    block2 = (dpi(x, 0) + (-dpi(x, -1) / (di(x, -1) - 1) / (di(x, -1) - 1))) / (
        Si(x, 1) + Ti(x, 2)
    )
    block3 = (cpi(x, 0) + (-cpi(x, -1) / (ci(x, -1) - 1) / (ci(x, -1) - 1))) / (
        Pi(x, 1) + Qi(x, 2)
    )
    return (block1 + block2 - block3) * M(2, 1, x)
