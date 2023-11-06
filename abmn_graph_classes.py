import numpy as np

class LineGraph:
        
    def __init__(
            self, 
            left=6, 
            right=6, 
            time_steps=100, 
            maxi_reward=100000, 
            mina_reward=99994
        ):
        self.left_end = left     # left endpoint: -k
        self.right_end = right      # right endpoint: l
        self.length = self.left + self.right + 1    # total length: k+l
        self.time_steps = time_steps   # Time steps

        # Note: position index i will be shifted
        # before: left end = -k, middle = 0, right end = l
        # now: left end = 0, middle = k, right end = k + l (= L)

        self.n_lambda = mina_reward
        self.m_lambda = maxi_reward


        # initialize the m,n values at time t=0, 
        # then iterate starting from t=1, use m(t-1), n(t-1) to compute a(t) and b(t) 
        # then use a(t) and b(t) to compute m(t) and n(t)

        # Each matrix: vertical axis (rows): time step, horizontal axis (colunmns): position
        # Therefore, m[t][i] access m value at time t, position index i
        self.a = np.zeros((self.time_steps, self.length))
        self.b = np.zeros((self.time_steps, self.length))
        self.m = np.zeros((self.time_steps, self.length))
        self.n = np.zeros((self.time_steps, self.length))

        # Initialize positional boundary values
        self.n[:, 0] = self.n_lambda
        self.m[:, -1] = self.m_lambda

        initial_ratio = np.arctan(np.linspace(
            -self.left_end, self.right_end, self.length-2) * 0.5) / np.pi + 0.5
        self.m[0, 1:-1] = self.m_lambda * initial_ratio
        self.n[0, 1:-1] = self.n_lambda * (1 - initial_ratio)

    def iterateABMN(self, t, debug=False):
        for i in range(1, self.length - 1):
            delta_m = self.m[t-1][i+1] - self.m[t-1][i-1]
            delta_n = self.n[t-1][i-1] - self.n[t-1][i+1]
            # Compute a,b using previous m,n
            self.b[t][i] = delta_m / (delta_m / delta_n + 1) \
                / (delta_m / delta_n + 1)
            self.a[t][i] = (delta_m / delta_n) * self.b[t][i]
            # Compute current m,n using current a,b
            maxi_wager_ratio = self.a[t][i] / (self.a[t][i] + self.b[t][i])
            mina_wager_ratio = self.b[t][i] / (self.a[t][i] + self.b[t][i])
            self.m[t][i] = maxi_wager_ratio * self.m[t-1][i+1] \
                + mina_wager_ratio * self.m[t-1][i-1] - self.a[t][i]
            self.n[t][i] = maxi_wager_ratio * self.n[t-1][i+1] \
                + mina_wager_ratio * self.n[t-1][i-1] - self.b[t][i]
        
        if debug:
            print(f"-------------- step {t} --------------")
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))
            print("delta_m = {}, delta_n = {}".format(delta_m, delta_n))

    def solve(self, debug=False):
        for t in range(1, self.time_steps):
            if t % (self.time_steps // 10) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)


class OriginCrossGraph:

    def __init__(
            self,
            left=6,
            right=6,
            top=6,
            bottom=6,
            time_steps=100,
            horizontal_maxi_reward=100000,
            horizontal_mina_reward=99994,
            vertical_maxi_reward=100000,
            vertical_mina_reward=99994
    ):
        self.right_end = left + right
        self.bottom_end = top + bottom
        self.origin = (top, left)
        self.horizontal_length = self.right_end + 1
        self.vertical_length = self.bottom_end + 1
        self.time_steps = time_steps
        self.horizontal_m_lambda = horizontal_maxi_reward
        self.horizontal_n_lambda = horizontal_mina_reward
        self.vertical_m_lambda = vertical_maxi_reward    
        self.vertical_n_lambda = vertical_mina_reward

        self.a = np.zeros((
            self.time_steps,
            self.vertical_length,
            self.horizontal_length))
        self.b = self.a.copy()
        self.m = self.a.copy()
        self.n = self.a.copy()
        self.m[:, self.origin[0], -1] = self.horizontal_m_lambda
        self.m[:, -1, self.origin[1]] = self.vertical_m_lambda
        self.n[:, self.origin[0], 0] = self.horizontal_n_lambda
        self.n[:, 0, self.origin[1]] = self.vertical_n_lambda
        horizontal_initial_ratio = np.arctan(np.linspace(
            -left, right, self.horizontal_length-2) * 0.5) / np.pi + 0.5
        vertical_initial_ratio = np.arctan(np.linspace(
            -top, bottom, self.vertical_length-2) * 0.5) / np.pi + 0.5
        self.m[0, self.origin[0], 1:-1] = self.horizontal_m_lambda * horizontal_initial_ratio
        self.m[0, 1:-1, self.origin[1]] = self.vertical_m_lambda * vertical_initial_ratio
        self.n[0, self.origin[0], 1:-1] = self.horizontal_n_lambda * (1 - horizontal_initial_ratio)
        self.n[0, 1:-1, self.origin[1]] = self.vertical_n_lambda * (1 - vertical_initial_ratio)

    def find_next_move(self, t, i, j):
        m_max = {}
        m_max[(i-1, j)] = self.m[t-1, i-1, j]
        m_max[(i+1, j)] = self.m[t-1, i+1, j]
        m_max[(i, j-1)] = self.m[t-1, i, j-1]
        m_max[(i, j+1)] = self.m[t-1, i, j+1]

        n_max = {}
        n_max[(i-1, j)] = self.n[t-1, i-1, j]
        n_max[(i+1, j)] = self.n[t-1, i+1, j]
        n_max[(i, j-1)] = self.n[t-1, i, j-1]
        n_max[(i, j+1)] = self.n[t-1, i, j+1]
        v_plus = max(m_max, key=m_max.get)
        v_minus = max(n_max, key=n_max.get)

        return v_plus, v_minus
    
    def iterateABMN(self, t, debug=False):
        if debug:
            print(f"-------------- step {t} --------------")

        for i in range(1, self.vertical_length - 1):
            for j in range(1, self.horizontal_length - 1):
                if self.m[t - 1, i, j] == 0 and self.n[t - 1, i, j] == 0:
                    continue
                v_plus, v_minus = self.find_next_move(t, i, j)
                delta_m = self.m[t-1, *v_plus] - self.m[t-1, *v_minus]
                delta_n = self.n[t-1, *v_minus] - self.n[t-1, *v_plus]
                self.b[t, i, j] = delta_m / (delta_m / delta_n + 1) \
                    / (delta_m / delta_n + 1)
                self.a[t, i, j] = (delta_m / delta_n) * self.b[t, i, j]
                maxi_wager_ratio = self.a[t, i, j] / (self.a[t, i, j] + self.b[t, i, j])
                mina_wager_ratio = self.b[t, i, j] / (self.a[t, i, j] + self.b[t, i, j])
                self.m[t, i, j] = maxi_wager_ratio * self.m[t-1, *v_plus] \
                    + mina_wager_ratio * self.m[t-1, *v_minus] - self.a[t, i, j]
                self.n[t, i, j] = maxi_wager_ratio * self.n[t-1, *v_plus] \
                    + mina_wager_ratio * self.n[t-1, *v_minus] - self.b[t, i, j]
                
                if debug:
                    print("current position: ({}, {}), v_plus = {}, v_minus = {}, delta_m = {}, delta_n = {}"\
                          .format(i, j, v_plus, v_minus, delta_m, delta_n))
                    
        if debug:
            print("a = {}".format(self.a[t]))
            print("b = {}".format(self.b[t]))
            print("m = {}".format(self.m[t]))
            print("n = {}".format(self.n[t]))
    
    def solve(self, debug=False):
        for t in range(1, self.time_steps):
            if t % max((self.time_steps // 10), 1) == 0:
                self.iterateABMN(t, debug)
            else:
                self.iterateABMN(t)