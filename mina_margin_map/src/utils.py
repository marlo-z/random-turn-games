import math

import matplotlib.pyplot as plt
import numpy as np


def round_up(number):
    return math.nextafter(number, math.inf)


def round_down(number):
    return math.nextafter(number, -math.inf)


def plot(func, start, end, **kwargs):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [func(**kwargs, x=i) for i in x]
    plt.plot(x, y)
    plt.show()


def func_deriv_approx(func):
    def wrapper(x, **kwargs):
        return (func(**kwargs, x=x + 1e-8) - func(**kwargs, x=x)) / 1e-8

    return wrapper


def my_bisection(f, a, b, tol):
    # approximates a root, R, of f bounded
    # by a and b to within tolerance
    # | f(m) | < tol with m the midpoint
    # between a and b Recursive implementation

    # check if a and b bound a root
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception("The scalars a and b do not bound a root")

    # get midpoint
    m = (a + b) / 2

    if np.abs(f(m)) < tol:
        # stopping condition, report m as root
        return m
    elif np.sign(f(a)) == np.sign(f(m)):
        # case where m is an improvement on a.
        # Make recursive call with a = m
        return my_bisection(f, m, b, tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # case where m is an improvement on b.
        # Make recursive call with b = m
        return my_bisection(f, a, m, tol)
