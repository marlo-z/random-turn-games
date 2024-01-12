import math
import matplotlib.pyplot as plt
import numpy as np

w_max = 5
w_min = 1.914854215512675
s_max = 3
s_min = 0.02347088957957744


def round_up(number, decimals=10):
    multiplier = 10 ** decimals
    return math.ceil(number * multiplier) / multiplier


def round_down(number, decimals=10):
    multiplier = 10 ** decimals
    return math.floor(number * multiplier) / multiplier


''' Basis functions '''


def w(x):
    return (8 * x + 1) ** (1/2)


def upw(x):
    return round_up(w(x))


def downw(x):
    return round_down(w(x))


def s(x):
    return ((w(x) - 1) ** 2) / (4 * (w(x) + 7))


def ups(x):
    return round_up(((upw(x) - 1) ** 2) / (4 * (downw(x) + 7)))


def downs(x):
    return round_down(((downw(x) - 1) ** 2) / (4 * (upw(x) + 7)))


def sm(x):
    return 1 / s(1 / x)


def upsm(x):
    return round_up(1 / downs(1 / x))


def downsm(x):
    return round_down(1 / ups(1 / x))


'''Indexed basis functions'''


def si(x, i=0):
    if i == 0:
        return x
    elif i > 0:
        inner = si(x, i - 1)
        return s(inner)
    else:
        inner = si(x, i + 1)
        return sm(inner)


def upsi(x, i=0):
    if i == 0:
        return x
    elif i > 0:
        inner = upsi(x, i - 1)
        return ups(inner)
    else:
        inner = upsi(x, i + 1)
        return upsm(inner)


def downsi(x, i=0):
    if i == 0:
        return x
    elif i > 0:
        inner = downsi(x, i - 1)
        return downs(inner)
    else:
        inner = downsi(x, i + 1)
        return downsm(inner)


def ci(x, i=0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / 16


def upci(x, i=0):
    inner = upsi(x, i)
    return round_up(((upw(inner) + 3) ** 2) / 16)


def downci(x, i=0):
    inner = downsi(x, i)
    return round_down(((downw(inner) + 3) ** 2) / 16)


def di(x, i=0):
    inner = si(x, i)
    return ((w(inner) + 3) ** 2) / (8 * (w(inner) + 1))


def updi(x, i=0):
    innerup = upsi(x, i)
    innerdown = downsi(x, i)
    return round_up(((upw(innerup) + 3) ** 2) / (8 * (downw(innerdown) + 1)))


def downdi(x, i=0):
    innerup = upsi(x, i)
    innerdown = downsi(x, i)
    return round_down(((downw(innerdown) + 3) ** 2) / (8 * (upw(innerup) + 1)))


'''Memoized indexed basis functions'''


def si_memo(x, memo, i=0):
    if i == 0:
        return x
    elif i > 0:
        if f"s{i-1}" in memo:
            inner = memo[f"s{i-1}"]
        else:
            inner = si(x, memo, i - 1)
            memo[f"s{i-1}"] = inner
        return s(inner)
    else:
        if f"s{i+1}" in memo:
            inner = memo[f"s{i+1}"]
        else:
            inner = si(x, memo, i + 1)
            memo[f"s{i+1}"] = inner
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


'''Composite functions'''


def Pi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Pi(x, i - 1) + math.prod([ci(x, j) - 1 for j in range(0, i)])


def upPi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return upPi(x, i - 1) + round_up(math.prod([upci(x, j) - 1 for j in range(0, i)]))


def downPi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return downPi(x, i - 1) + round_down(math.prod([downci(x, j) - 1 for j in range(0, i)]))


def Si(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return Si(x, i - 1) + math.prod([di(x, j) - 1 for j in range(0, i)])


def upSi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return upSi(x, i - 1) + round_up(math.prod([updi(x, j) - 1 for j in range(0, i)]))


def downSi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0:
        return 1
    else:
        return downSi(x, i - 1) + round_down(math.prod([downdi(x, j) - 1 for j in range(0, i)]))


def Qi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Qi(x, i - 1) + math.prod([1 / (ci(x, -j) - 1) for j in range(1, i)])


def upQi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return upQi(x, i - 1) + round_up(math.prod([1 / (downci(x, -j) - 1) for j in range(1, i)]))


def downQi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return downQi(x, i - 1) + round_down(math.prod([1 / (upci(x, -j) - 1) for j in range(1, i)]))


def Ti(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return Ti(x, i - 1) + math.prod([1 / (di(x, -j) - 1) for j in range(1, i)])


def upTi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return upTi(x, i - 1) + round_up(math.prod([1 / (downdi(x, -j) - 1) for j in range(1, i)]))


def downTi(x, i=0):
    if i < 0:
        raise ValueError("i must be greater than or equal to 0")
    elif i == 0 or i == 1:
        return 0
    else:
        return downTi(x, i - 1) + round_down(math.prod([1 / (updi(x, -j) - 1) for j in range(1, i)]))


def Ai(x, i=0):
    return np.prod([di(x, n) - 1 for n in range(0, i + 1)])


def Bi(x, i=0):
    return np.prod([ci(x, n) - 1 for n in range(0, i + 1)])


def Ci(x, i=0):
    return np.prod([1 / (di(x, -n) - 1) for n in range(1, i + 1)])


def Di(x, i=0):
    return np.prod([1 / (ci(x, -n) - 1) for n in range(1, i + 1)])


def Ei(x, i=0):
    return sum([dpi(x, j) / (di(x, j) - 1) for j in range(0, i + 1)])


def Fi(x, i=0):
    return sum([cpi(x, j) / (ci(x, j) - 1) for j in range(0, i + 1)])


def Gi(x, i=0):
    return sum([-dpi(x, -j) / (di(x, -j) - 1) for j in range(1, i + 1)])


def Hi(x, i=0):
    return sum([-cpi(x, -j) / (ci(x, -j) - 1) for j in range(1, i + 1)])


'''Memoized composite functions'''


def Pi_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0:
            return 1
        else:
            return wrapper(x, i - 1) + math.prod([ci_memo(x, memo, j) - 1 for j in range(0, i)])
    return wrapper(x, i)


def Si_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0:
            return 1
        else:
            return wrapper(x, i - 1) + math.prod([di_memo(x, memo, j) - 1 for j in range(0, i)])
    return wrapper(x, i)


def Qi_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0 or i == 1:
            return 0
        else:
            return wrapper(x, i - 1) + math.prod([1 / (ci_memo(x, memo, -j) - 1) for j in range(1, i)])
    return wrapper(x, i)


def Ti_memo(x, i=0):
    memo = {}

    def wrapper(x, i):
        if i < 0:
            raise ValueError("i must be greater than or equal to 0")
        elif i == 0 or i == 1:
            return 0
        else:
            return wrapper(x, i - 1) + math.prod([1 / (di_memo(x, memo, -j) - 1) for j in range(1, i)])
    return wrapper(x, i)


'''Mina margin map'''


def M(l, k, x):
    return (x * (Si(x, k) + Ti(x, l))) / (Pi(x, k) + Qi(x, l))


'''Memorized Mina margin map'''


def M_memo(l, k, x):
    return (x * (Si_memo(x, k) + Ti_memo(x, l))) / (Pi_memo(x, k) + Qi_memo(x, l))


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


def spi(x, i=0):
    if i == 0:
        return 1
    elif i > 0:
        return sp(si(x, i - 1)) * spi(x, i - 1)
    else:
        return smp(si(x, i + 1)) * spi(x, i + 1)


def cpi(x, i=0):
    return cp(si(x, i)) * spi(x, i)


def dpi(x, i=0):
    return dp(si(x, i)) * spi(x, i)


'''Mina margin map derivative'''


def Mp(l, k, x):
    b1 = 1 / x
    b2 = block2(l, k, x)
    b3 = block3(l, k, x)

    return (b1 + b2 - b3) * M(l, k, x)


def block2(l, k, x):
    return (sum([Ei(x, i) * Ai(x, i) for i in range(k)])
            + sum([Gi(x, i) * Ci(x, i) for i in range(1, l - 1)])) \
        / (Si(x, k) + Ti(x, l))


def block3(l, k, x):
    return (sum([Fi(x, i) * Bi(x, i) for i in range(k)])
            + sum([Hi(x, i) * Di(x, i) for i in range(1, l - 1)])) \
        / (Pi(x, k) + Qi(x, l))


'''M21 derivative'''


def M21p(x):
    block1 = 1/x
    block2 = (dpi(x, 0) + (-dpi(x, -1) / (di(x, -1) - 1) /
              (di(x, -1) - 1))) / (Si(x, 1) + Ti(x, 2))
    block3 = (cpi(x, 0) + (-cpi(x, -1) / (ci(x, -1) - 1) /
              (ci(x, -1) - 1))) / (Pi(x, 1) + Qi(x, 2))
    return (block1 + block2 - block3) * M(2, 1, x)


'''Function derivative approximation wrapper'''


def funcp_approx(func):
    def wrapper(x, **kwargs):
        return (func(**kwargs, x=x + 1e-4) - func(**kwargs, x=x)) / 1e-4
    return wrapper


'''Function plotter'''


def plot(func, start, end, **kwargs):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [func(**kwargs, x=i) for i in x]
    plt.plot(x, y)
    plt.show()


def plot_w_bound(start, end, n_partition):
    x = [i for i in np.arange(start, end, (end - start) / 1e4)]
    y = [M(5, 4, i) for i in x]
    mesh = (end - start) / n_partition
    x_part = [i for i in np.arange(start, end, mesh)]
    y_up = [(i + mesh) * (Si(i + mesh, 4) + Ti(i, 5))
            / (Pi(i + mesh, 4) + Qi(i, 5)) for i in x_part]
    y_low = [(i) * (Si(i, 4) + Ti(i + mesh, 5))
             / (Pi(i + mesh, 4) + Qi(i, 5)) for i in x_part]
    plt.plot(x, y)
    plt.plot(x_part, y_up)
    plt.plot(x_part, y_low)
    plt.show()


def Mp54_wrapper(func):
    def wrapper(x):
        return func(5, 4, x)
    return wrapper


'''Bisection method'''


def my_bisection(f, a, b, tol):
    # approximates a root, R, of f bounded
    # by a and b to within tolerance
    # | f(m) | < tol with m the midpoint
    # between a and b Recursive implementation

    # check if a and b bound a root
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception(
            "The scalars a and b do not bound a root")

    # get midpoint
    m = (a + b)/2

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


'''Min max variables'''
min_max_dict = {}

'''w,s max and min'''
min_max_dict["w_max"] = 5
min_max_dict["w_min"] = 1.914854215512675
min_max_dict["s_max"] = 1/3
min_max_dict["s_min"] = 0.023470889579577447

'''s_j max and min'''
min_max_dict["sm4_max"] = 2070264293599548.8
min_max_dict["sm3_max"] = 32173467.370981574
min_max_dict["sm2_max"] = 4008.5780621967074
min_max_dict["sm1_max"] = 42.6059692628831
min_max_dict["s0_max"] = 3
min_max_dict["s1_max"] = 0.3333333333333333
min_max_dict["s2_max"] = 0.023470889579577447
min_max_dict["s3_max"] = 0.0002494650183890889
min_max_dict["s4_max"] = 3.108151162165184e-08

min_max_dict["sm4_min"] = 32173467.370981574
min_max_dict["sm3_min"] = 4008.5780621967074
min_max_dict["sm2_min"] = 42.6059692628831
min_max_dict["sm1_min"] = 3.0
min_max_dict["s0_min"] = 0.3333333333333333
min_max_dict["s1_min"] = 0.023470889579577447
min_max_dict["s2_min"] = 0.0002494650183890889
min_max_dict["s3_min"] = 3.108151162165184e-08
min_max_dict["s4_min"] = 4.830301150880159e-16


'''c_j max and min'''
min_max_dict["cm4_max"] = 1035132195059979.4
min_max_dict["cm3_max"] = 16092750.551088786
min_max_dict["cm2_max"] = 2072.0690081661132
min_max_dict["cm1_max"] = 28.86140661634507
min_max_dict["c0_max"] = 4
min_max_dict["c1_max"] = 1.5097369974839203
min_max_dict["c2_max"] = 1.0454281787318354
min_max_dict["c3_max"] = 1.000498743524459
min_max_dict["c4_max"] = 1.0000000621630205

min_max_dict["cm4_min"] = 16092750.551088786
min_max_dict["cm3_min"] = 2072.0690081661132
min_max_dict["cm2_min"] = 28.86140661634507
min_max_dict["cm1_min"] = 4
min_max_dict["c0_min"] = 1.5097369974839203
min_max_dict["c1_min"] = 1.0454281787318354
min_max_dict["c2_min"] = 1.000498743524459
min_max_dict["c3_min"] = 1.0000000621630205
min_max_dict["c4_min"] = 1.0000000000000009


'''d_j max and min'''
min_max_dict["dm4_max"] = 16086735.43042101
min_max_dict["dm3_max"] = 2006.0385638291439
min_max_dict["dm2_max"] = 23.01276890062102
min_max_dict["dm1_max"] = 2.961795994671831
min_max_dict["d0_max"] = 1.3333333333333333
min_max_dict["d1_max"] = 1.0358919423477113
min_max_dict["d2_max"] = 1.0004828424335728
min_max_dict["d3_max"] = 1.0000000621397853
min_max_dict["d4_max"] = 1.000000000000001

min_max_dict["dm4_min"] = 2006.0385638291439
min_max_dict["dm3_min"] = 23.01276890062102
min_max_dict["dm2_min"] = 2.961795994671831
min_max_dict["dm1_min"] = 1.3333333333333333
min_max_dict["d0_min"] = 1.0358919423477113
min_max_dict["d1_min"] = 1.0004828424335728
min_max_dict["d2_min"] = 1.0000000621397853
min_max_dict["d3_min"] = 1.000000000000001
min_max_dict["d4_min"] = 1.0


'''sp, dp, cp max and min'''
min_max_dict["sp_max"] = 0.12398081817324916    # w \approx 3.2099, w \in [3.2, 3.3]
# w \approx 2.06418, w \in [2, 2.1]
min_max_dict["dp_max"] = 0.15089688320697686
min_max_dict["cp_max"] = 2     # w \approx 1.91485, w \in [1.9, 2]


'''sp max and min, need double check negative index cases'''
min_max_dict["smp4_max"] = 7597254302896108.0
min_max_dict["smp3_max"] = 59033532.904424794
min_max_dict["smp2_max"] = 3679.634977826626
min_max_dict["smp1_max"] = 20.50946521745262
min_max_dict["sp0_max"] = 1
min_max_dict["sp1_max"] = 0.12398081817324916
min_max_dict["sp2_max"] = 0.012606962016215263
min_max_dict["sp3_max"] = 0.0002555177386208926
min_max_dict["sp4_max"] = 6.363558581158948e-08

min_max_dict["smp4_min"] = 531301796.13982326
min_max_dict["smp3_min"] = 33116.71480043964
min_max_dict["smp2_min"] = 184.5851869570736
min_max_dict["smp1_min"] = 9.0
min_max_dict["sp0_min"] = 1
min_max_dict["sp1_min"] = 0.10168477835497472
min_max_dict["sp2_min"] = 0.0020609457364915555
min_max_dict["sp3_min"] = 5.132696069376309e-07
min_max_dict["sp4_min"] = 1.595319191111739e-14


'''cp max and min'''
min_max_dict["cmp4_max"] = 3799337471368903.5
min_max_dict["cmp3_max"] = 30011240.037174445
min_max_dict["cmp2_max"] = 2138.341750026244
min_max_dict["cmp1_max"] = 16.407572173962098
min_max_dict["cp0_max"] = 1.2833494518006403
min_max_dict["cp1_max"] = 0.23263012061215851
min_max_dict["cp2_max"] = 0.025195082253865478
min_max_dict["cp3_max"] = 0.0005110354295905288
min_max_dict["cp4_max"] = 1.272711716231788e-07

min_max_dict["cmp4_min"] = 265650904.26253483
min_max_dict["cmp3_min"] = 16561.45371124193
min_max_dict["cmp2_min"] = 93.83870624927889
min_max_dict["cmp1_min"] = 5.230158933211166
min_max_dict["cp0_min"] = 0.8
min_max_dict["cp1_min"] = 0.13049710455832642
min_max_dict["cp2_min"] = 0.003867034129305261
min_max_dict["cp3_min"] = 1.0257721050138527e-06
min_max_dict["cp4_min"] = 3.1906380847139413e-14


'''dp max and min, negative index cases are very loose because 
sm, smp optimize in opposite direction'''
min_max_dict["dmp4_max"] = 236773303270.587
min_max_dict["dmp3_max"] = 164804.19767536205
min_max_dict["dmp2_max"] = 98.46015365963227
min_max_dict["dmp1_max"] = 1.8230635748846775
min_max_dict["dp0_max"] = 0.15089688320697686
min_max_dict["dp1_max"] = 0.01713237783297246
min_max_dict["dp2_max"] = 0.0004866287596302319
min_max_dict["dp3_max"] = 1.271998163566851e-07
min_max_dict["dp4_max"] = 3.955779294589308e-15

min_max_dict["dmp4_min"] = 2.0642077252090254
min_max_dict["dmp3_min"] = 1.0321036579993048
min_max_dict["dmp2_min"] = 0.5153073540163661
min_max_dict["dmp1_min"] = 0.24082317628692868
min_max_dict["dp0_min"] = 0.08888888888888889
min_max_dict["dp1_min"] = 0.0039250326526335975
min_max_dict["dp2_min"] = 1.0259636791470255e-06
min_max_dict["dp3_min"] = 3.1906381590913157e-14
min_max_dict["dp4_min"] = 1.4169280780789018e-29


'''S, P, T, Q max and min'''
min_max_dict["S4_max"] = 1.345303090833859
min_max_dict["P4_max"] = 5.59871491008425
min_max_dict["T5_max"] = 4.598714910084252
min_max_dict["Q5_max"] = 0.345303090833859

min_max_dict["S4_min"] = 1.035909272501577
min_max_dict["P4_min"] = 1.532904970028801
min_max_dict["T5_min"] = 0.5329049700288012
min_max_dict["Q5_min"] = 0.03590927250157703


'''A, B, C, D max and min'''
min_max_dict["A0_max"] = 0.33333333333333326
min_max_dict["A1_max"] = 0.011963980782570435
min_max_dict["A2_max"] = 5.776717596274187e-06
min_max_dict["A3_max"] = 3.5896399127130776e-13

min_max_dict["A0_min"] = 0.035891942347711314
min_max_dict["A1_min"] = 1.7330152788822567e-05
min_max_dict["A2_min"] = 1.0768919738139236e-12
min_max_dict["A3_min"] = 1.195590264362249e-27

min_max_dict["B0_max"] = 3
min_max_dict["B1_max"] = 1.529210992451761
min_max_dict["B2_max"] = 0.06946927028378592
min_max_dict["B3_max"] = 3.464734870293026e-05

min_max_dict["B0_min"] = 0.5097369974839203
min_max_dict["B1_min"] = 0.023156423427928643
min_max_dict["B2_min"] = 1.1549116234310089e-05
min_max_dict["B3_min"] = 7.179279493328148e-13

min_max_dict["C1_max"] = 3.000000000000001
min_max_dict["C2_max"] = 1.5292109924517612
min_max_dict["C3_max"] = 0.06946927028378604
min_max_dict["C4_max"] = 3.464734870291789e-05

min_max_dict["C1_min"] = 0.5097369974839202
min_max_dict["C2_min"] = 0.02315642342792867
min_max_dict["C3_min"] = 1.154911623430596e-05
min_max_dict["C4_min"] = 7.179279476676054e-13

min_max_dict["D1_max"] = 0.3333333333333333
min_max_dict["D2_max"] = 0.01196398078257044
min_max_dict["D3_max"] = 5.776717596273765e-06
min_max_dict["D4_max"] = 3.589639904563686e-13

min_max_dict["D1_min"] = 0.03589194234771132
min_max_dict["D2_min"] = 1.7330152788821297e-05
min_max_dict["D3_min"] = 1.0768919713691058e-12
min_max_dict["D4_min"] = 1.0403424572324386e-27


'''E, F, G, H max and min'''
min_max_dict["E0_max"] = 4.204199420168715
min_max_dict["E1_max"] = 39.68653618622748
min_max_dict["E2_max"] = 7870.8812714943115
min_max_dict["E3_max"] = 114579279.990384

min_max_dict["E0_min"] = 0.2666666666666667
min_max_dict["E1_min"] = 0.3760235973841229
min_max_dict["E2_min"] = 0.3781484389635082
min_max_dict["E3_min"] = 0.37814895242491503

min_max_dict["F0_max"] = 2.517669814306786
min_max_dict["F1_max"] = 7.638502898665833
min_max_dict["F2_max"] = 58.1556144364953
min_max_dict["F3_max"] = 8279.046835730309

min_max_dict["F0_min"] = 0.26666666666666666
min_max_dict["F1_min"] = 0.5226753637054625
min_max_dict["F2_min"] = 0.6077994923246736
min_max_dict["F3_min"] = 0.6098562049529258

min_max_dict["G1_max"] = -0.12275648280503984
min_max_dict["G2_max"] = -0.1461659573851245
min_max_dict["G3_max"] = -0.1466807124011219
min_max_dict["G4_max"] = -0.14668084071850876

min_max_dict["G1_min"] = -5.469190724654034
min_max_dict["G2_min"] = -55.65797382292041
min_max_dict["G3_min"] = -7542.412521576003
min_max_dict["G4_min"] = -118096694.18345143

min_max_dict["H1_max"] = -0.18772056290018252
min_max_dict["H2_max"] = -0.2330298721889015
min_max_dict["H3_max"] = -0.23405899736472463
min_max_dict["H4_max"] = -0.23405925399948638

min_max_dict["H1_min"] = -5.469190724654033
min_max_dict["H2_min"] = -82.2184295363001
min_max_dict["H3_min"] = -14572.918603621156
min_max_dict["H4_min"] = -236104587.20157942


'''Mp_5,4 components'''
min_max_dict["block1_max"] = 3
min_max_dict["block1_min"] = 1/3

min_max_dict["block2_max"] = 0.8412307805797564
min_max_dict["block2_min"] = -0.6989049746548016

min_max_dict["block3_max"] = 14.976536856282161
min_max_dict["block3_min"] = -0.008358752316897694

min_max_dict["M54_max"] = 11.366580898700018
min_max_dict["M54_min"] = 0.08797720342749411

Mp52_max = 43.75667085245863
Mp52_min = -1.3497558003003605
