import math
import matplotlib.pyplot as plt
import numpy as np

w_max = 5
w_min = 1.914854215512675
s_max = 3
s_min = 0.02347088957957744

''' Basis functions '''
def w(x):
    return (8 * x + 1) ** (1/2)

def s(x):
    return ((w(x) - 1) ** 2) / (4 * (w(x) + 7))

def sm(x):
    return 1 / s(1 / x)


'''Indexed basis functions'''
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


'''Composite functions'''
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
    
def Ai(x, i = 0):
    return np.prod([di(x, n) - 1 for n in range(0, i + 1)])

def Bi(x, i = 0):
    return np.prod([ci(x, n) - 1 for n in range(0, i + 1)])

def Ci(x, i = 0):
    return np.prod([1 / (di(x, -n) - 1) for n in range(1, i + 1)])

def Di(x, i = 0):
    return np.prod([1 / (ci(x, -n) - 1) for n in range(1, i + 1)])

def Ei(x, i = 0):
    return sum([dpi(x, j) / (di(x, j) - 1) for j in range(0, i + 1)])

def Fi(x, i = 0):
    return sum([cpi(x, j) / (ci(x, j) - 1) for j in range(0, i + 1)])

def Gi(x, i = 0):
    return sum([-dpi(x, -j) / (di(x, -j) - 1) for j in range(1, i + 1)])

def Hi(x, i = 0):
    return sum([-cpi(x, -j) / (ci(x, -j) - 1) for j in range(1, i + 1)])

'''Mina margin map'''
def M(l, k, x):
    return (x * (Si(x, k) + Ti(x, l))) / (Pi(x, k) + Qi(x, l))


'''Basis function derivatives'''
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


'''Indexed basis function derivatives'''
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


'''Mina margin map derivative'''
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


'''M21 derivative'''
def M21p(x):
    block1 = 1/x
    block2 = (dpi(x, 0) + (-dpi(x, -1) / (di(x, -1) - 1) / (di(x, -1) - 1))) / (Si(x, 1) + Ti(x, 2))
    block3 = (cpi(x, 0) + (-cpi(x, -1) / (ci(x, -1) - 1) / (ci(x, -1) - 1))) / (Pi(x, 1) + Qi(x, 2))
    return (block1 + block2 - block3) * M(2, 1, x)


'''Function derivative approximation wrapper'''
def funcp_approx(func):
    def wrapper(x, **kwargs):
        return (func(**kwargs, x = x + 1e-4) - func(**kwargs, x = x)) / 1e-4
    return wrapper


'''Function plotter'''
def plot(func, start, end, **kwargs):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [func(**kwargs, x = i) for i in x]
    plt.plot(x, y)
    plt.show()



'''Min max variables'''
w_max = 5
w_min = 1.914854215512675
s_max = 1/3
s_min = 0.023470889579577447

cm4_max = 1035132195059979.4
cm4_min = 16092750.551088786
cm3_max = 16092750.551088786
cm3_min = 2072.0690081661132
cm2_max = 2072.0690081661132
cm2_min = 28.86140661634507
cm1_max = 28.86140661634507
cm1_min = 4
c0_max = 4
c0_min = 1.5097369974839203
c1_max = 1.5097369974839203
c1_min = 1.0454281787318354
c2_max = 1.0454281787318354
c2_min = 1.000498743524459
c3_max = 1.000498743524459
c3_min = 1.0000000621630205
c4_max = 1.0000000621630205
c4_min = 1.0000000000000009

dm4_max = 16086735.43042101
dm4_min = 2006.0385638291439
dm3_max = 2006.0385638291439
dm3_min = 23.01276890062102
dm2_max = 23.01276890062102
dm2_min = 2.961795994671831
dm1_max = 2.961795994671831
dm1_min = 1.3333333333333333
d0_max = 1.3333333333333333
d0_min = 1.0358919423477113
d1_max = 1.0358919423477113
d1_min = 1.0004828424335728
d2_max = 1.0004828424335728
d2_min = 1.0000000621397853
d3_max = 1.0000000621397853
d3_min = 1.000000000000001
d4_max = 1.000000000000001
d4_min = 1.0

S4_max = 1.345303090833859
S4_min = 1.035909272501577
P4_max = 5.59871491008425
P4_min = 1.532904970028801
T5_max = 4.598714910084252
T5_min = 0.5329049700288012
Q5_max = 0.345303090833859
Q5_min = 0.03590927250157703

M54_max = 11.366580898700018
M54_min = 0.08797720342749411