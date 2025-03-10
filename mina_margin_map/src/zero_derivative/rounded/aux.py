from ...utils import round_down, round_up
from ..aux import w


def upw(x):
    return round_up(w(x))


def downw(x):
    return round_down(w(x))


def ups(x):
    return round_up(((upw(x) - 1) ** 2) / (4 * (downw(x) + 7)))


def downs(x):
    return round_down(((downw(x) - 1) ** 2) / (4 * (upw(x) + 7)))


def upsm(x):
    return round_up(1 / downs(1 / x))


def downsm(x):
    return round_down(1 / ups(1 / x))
