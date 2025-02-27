from ...utils import round_down, round_up
from ...zero_derivative.rounded import downsm, downw, upsm, upw


def upwp(x):
    return round_up(4 / round_down(round_down(8 * x + 1) ** (1 / 2)))


def downwp(x):
    return round_down(4 / round_up(round_up(8 * x + 1) ** (1 / 2)))


def upsp(x):
    return round_up(
        upwp(x) * (upw(x) - 1) * (upw(x) + 15) / round_down(4 * (downw(x) + 7) ** 2)
    )


def downsp(x):
    return round_down(
        downwp(x) * (downw(x) - 1) * (downw(x) + 15) / round_up(4 * (upw(x) + 7) ** 2)
    )


def upsmp(x):
    return round_up(upsp(1 / x) * upsm(x) ** 2) / round_down(x**2)


def downsmp(x):
    return round_down(downsp(1 / x) * downsm(x) ** 2) / round_up(x**2)


def upcp(x):
    return upwp(x) * (upw(x) + 3) / 8


def downcp(x):
    return downwp(x) * (downw(x) + 3) / 8


def updp(x):
    return upwp(x) * (upw(x) + 3) * (upw(x) - 1) / (8 * round_down((downw(x) + 1) ** 2))


def downdp(x):
    return (
        downwp(x) * (downw(x) + 3) * (downw(x) - 1) / (8 * round_up((upw(x) + 1) ** 2))
    )
