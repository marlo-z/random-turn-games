# Test
import numpy as np
from matplotlib import pyplot as plt
k = 6      # left endpoint: -k
l = 6      # right endpoint: l
L = k+l+1    # total length: k+l
T = 100    # Time steps

# Note: position index i will be shifted
# before: left end = -k, middle = 0, right end = l
# now: left end = 0, middle = k, right end = k + l (= L)

_lambda = 0.6

# initialize the m,n values are time t=0,
# then iterate starting from t=1, use m(t-1), n(t-1) to compute a(t) and b(t)
# then use a(t) and b(t) to compute m(t) and n(t)

# Each matrix: vertical axis (rows): time step, horizontal axis (colunmns): position
# Therefore, m[t][i] access m value at time t, position index i
a = np.zeros(T*L).reshape((T, L))
b = np.zeros(T*L).reshape((T, L))
m = np.zeros(T*L).reshape((T, L))
n = np.zeros(T*L).reshape((T, L))

# Initialize positional boundary values
for t in range(a.shape[0]):
    n[t][0] = 1
    m[t][0] = 0
    n[t][L-1] = 0
    m[t][L-1] = _lambda

# Initialize time boundary values
for i in range(L):
    m[0][i] = (_lambda / (L-1)) * i
    n[0][i] = (1 / (L-1)) * ((L-1) - i)

# Recursive solving algorithm

for t in range(1, T):
    for i in range(1, L-1):
        delta_m = m[t-1][i+1] - m[t-1][i-1]
        delta_n = n[t-1][i-1] - n[t-1][i+1]
        # Compute a,b using previous m,n
        b[t][i] = delta_m / (((delta_m / delta_n) + 1)**2)
        a[t][i] = (delta_m / delta_n) * b[t][i]
        print(a[t][i], b[t][i])
        # Compute current m,n using current a,b
        m[t][i] = (a[t][i]/(a[t][i] + b[t][i]))*m[t-1][i+1] + \
            (b[t][i]/(a[t][i] + b[t][i]))*m[t-1][i-1] - a[t][i]
        n[t][i] = (a[t][i]/(a[t][i] + b[t][i]))*n[t-1][i+1] + \
            (b[t][i]/(a[t][i] + b[t][i]))*n[t-1][i-1] - n[t][i]
