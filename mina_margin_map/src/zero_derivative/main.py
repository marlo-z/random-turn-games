import numpy as np
from matplotlib import pyplot as plt

from ..utils import round_down, round_up
from .indexed_aux import Pi, Qi, Si, Ti
from .memo_indexed_aux import Pi_memo, Qi_memo, Si_memo, Ti_memo
from .rounded import (
    downci,
    downPi,
    downQi,
    downSi,
    downsi,
    downTi,
    upci,
    upPi,
    upQi,
    upSi,
    upsi,
    upTi,
)


def M(l, k, x):
    return (x * (Si(x, k) + Ti(x, l))) / (Pi(x, k) + Qi(x, l))


def calculate_bounds(l, k, x, mesh):
    upper = (x + mesh) * (Si(x + mesh, k) + Ti(x, l)) / (Pi(x, k) + Qi(x + mesh, l))
    lower = x * (Si(x, k) + Ti(x + mesh, l)) / (Pi(x + mesh, k) + Qi(x, l))
    return upper, lower


def calculate_rounded_bounds(l, k, x, mesh):
    upper = round_up(
        (x + mesh)
        * (upSi(x + mesh, k) + upTi(x, l))
        / (downPi(x, k) + downQi(x + mesh, l))
    )
    lower = round_down(
        x * (downSi(x, k) + downTi(x + mesh, l)) / (upPi(x + mesh, k) + upQi(x, l))
    )
    return upper, lower


def print_table(x):
    for i in range(-4, 4):
        s1 = upsi(x, i)
        s2 = downsi(x, i)
        print(f"i = {i}; s_i up {s1}; s_i down {s2}")
    for i in range(-4, 4):
        c1 = upci(x, i)
        c2 = downci(x, i)
        d1 = upci(x, i)
        d2 = downci(x, i)
        print(f"i = {i}; c_i up {c1}; c_i down {c2}; d_i up {d1}; d_i down {d2}")
    S1 = upSi(x, 4)
    S2 = downSi(x, 4)
    T1 = upTi(x, 5)
    T2 = downTi(x, 5)
    P1 = upPi(x, 4)
    P2 = downPi(x, 4)
    Q1 = upQi(x, 5)
    Q2 = downQi(x, 5)
    print(f"S4 up = {S1}; S4 down = {S2}")
    print(f"T5 up = {T1}; T5 down = {T2}")
    print(f"P4 up = {P1}; P4 down = {P2}")
    print(f"Q5 up = {Q1}; Q5 down = {Q2}")
    M1 = round_up((x) * (upSi(x, 4) + upTi(x, 5)) / (downPi(x, 4) + downQi(x, 5)))
    M2 = round_down(x * (downSi(x, 4) + downTi(x, 5)) / (upPi(x, 4) + upQi(x, 5)))
    print(f"M up = {M1}; M down = {M2}")


"""Memorized Mina margin map"""


def M_memo(l, k, x):
    return (x * (Si_memo(x, k) + Ti_memo(x, l))) / (Pi_memo(x, k) + Qi_memo(x, l))


def plot_w_bound(start, end, n_partition):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [M(5, 4, i) for i in x]
    mesh = (end - start) / n_partition
    x_part = [i for i in np.arange(start, end, mesh)]
    y_up = [
        (i + mesh) * (Si(i + mesh, 4) + Ti(i, 5)) / (Pi(i + mesh, 4) + Qi(i, 5))
        for i in x_part
    ]
    y_low = [
        (i) * (Si(i, 4) + Ti(i + mesh, 5)) / (Pi(i + mesh, 4) + Qi(i, 5))
        for i in x_part
    ]
    plt.plot(x, y)
    plt.plot(x_part, y_up)
    plt.plot(x_part, y_low)
    plt.show()
