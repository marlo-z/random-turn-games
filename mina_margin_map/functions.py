import math
import matplotlib.pyplot as plt
import numpy as np

def w(x):
    return (8 * x + 1) ** (1/2)

def s(x):
    return ((w(x) - 1) ** 2) / (4 * (w(x) + 7))

def sm(x):
    return 1 / s(1 / x)

def si(x, i = 0):
    if i == 0:
        return x
    elif i > 0:
        inner = si(x, i - 1)
        return s(inner)
    else:
        inner = si(x, i + 1)
        return sm(inner)

def ci(x, i = 0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / 16

def di(x, i = 0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / (8 * (w(inner) + 1))

def Pi(x, i = 0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Pi(x, i - 1) + math.prod([ci(x, j) - 1 for j in range(0, i)])
    
def Si(x, i = 0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Si(x, i - 1) + math.prod([di(x, j) - 1 for j in range(0, i)])

def Qi(x, i = 0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Qi(x, i - 1) + math.prod([1 / (ci(x, -j) - 1) for j in range(1, i)])
    
def Ti(x, i = 0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Ti(x, i - 1) + math.prod([1 / (di(x, -j) - 1) for j in range(1, i)])
    
def M(l, k, x):
    return (x * (Si(x, k) + Ti(x, l))) / (Pi(x, k) + Qi(x, l))

def wp(x):
    return 4 / ((8 * x + 1) ** (1/2))

def sp(x):
    return wp(x) * (w(x) - 1) * (w(x) + 15) / (4 * (w(x) + 7) ** 2)

def smp(x):
    return sp(1/x) * sm(x) ** 2 / x ** 2

def cp(x):
    return wp(x) * (w(x) + 3) / 8

def dp(x):
    return wp(x) * (w(x) + 3) * (w(x) - 1) / (8 * (w(x) + 1) ** 2)

def spi(x, i = 0):
    if i == 0:
        return 1
    elif i > 0:
        return sp(si(x, i - 1)) * spi(x, i - 1)
    else:
        return smp(si(x, i + 1)) * spi(x, i + 1)
    
def cpi(x, i = 0):
    return cp(si(x, i)) * spi(x, i)

def dpi(x, i = 0):
    return dp(si(x, i)) * spi(x, i)

def Mp(l, k, x):
    block1 = 1 / x
    block2 = (sum([sum([dpi(x, j) / (di(x, j) - 1) for j in range(0, i + 1)]) \
                  * np.prod([di(x, n) - 1 for n in range(0, i + 1)]) \
                    for i in range(0, k)]) + \
             sum([sum([-dpi(x, -j) / (di(x, -j) - 1) for j in range(1, i + 1)]) \
                  * np.prod([1 / (di(x, -n) - 1) for n in range(1, i+1)]) \
                    for i in range(1, l)])) / (Si(x, k) + Ti(x, l))
    
    block3 = (sum([sum([cpi(x, j) / (ci(x, j) - 1) for j in range(0, i + 1)]) \
                  * np.prod([ci(x, n) - 1 for n in range(0, i + 1)]) \
                    for i in range(0, k)]) + \
             sum([sum([-cpi(x, -j) / (ci(x, -j) - 1) for j in range(1, i + 1)]) \
                  * np.prod([1 / (ci(x, -n) - 1) for n in range(1, i+1)]) \
                    for i in range(1, l)])) / (Pi(x, k) + Qi(x, l))
    
    return (block1 + block2 - block3) * M(l, k, x)

def funcp_approx(func):
    def wrapper(x, **kwargs):
        return (func(**kwargs, x = x + 1e-4) - func(**kwargs, x = x)) / 1e-4
    return wrapper

def plot(func, start, end, **kwargs):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [func(**kwargs, x = i) for i in x]
    plt.plot(x, y)
    plt.show()

def M21p(x):
    block1 = 1/x
    block2 = (dpi(x, 0) + (-dpi(x, -1) / (di(x, -1) - 1) / (di(x, -1) - 1))) / (Si(x, 1) + Ti(x, 2))
    block3 = (cpi(x, 0) + (-cpi(x, -1) / (ci(x, -1) - 1) / (ci(x, -1) - 1))) / (Pi(x, 1) + Qi(x, 2))
    return (block1 + block2 - block3) * M(2, 1, x)