from abmn_graph_classes import ContinuousGraphSolver
from functions import *
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot(x_dim, y_dim, a, b, T_steps):
    plt.rcParams["figure.figsize"] = [16, 10]
    plt.rcParams["figure.autolayout"] = True

    interval = 100

    x = np.arange(x_dim)
    y = np.arange(y_dim)
    xarray, yarray = np.meshgrid(x, y)
    # f = lambda x, y, sig: 1 / np.sqrt(sig) * np.exp(-((x-x_dim/2) ** 2 + (y-y_dim/2) ** 2) / sig ** 2)
    # zarray = np.zeros((x_dim, y_dim, T_steps))
    # for i in range(T_steps):
    #     zarray[:, :, i] = f(xarray, yarray, 1.5 + np.sin(i * 2 * np.pi / T_steps))
    #     zarray[:, :, i] = np.ones((x_dim, y_dim)) * i

    zarray_a = np.zeros((x_dim, y_dim, T_steps))
    zarray_b = np.zeros((x_dim, y_dim, T_steps))
    for i in range(T_steps):
        zarray_a[:, :, i] = a[i]
        zarray_b[:, :, i] = b[i]

    def change_plot(frame_number, zarray_a, zarray_b, plot):
        plot[0].remove()
        plot[1].remove()
        plot[0] = ax.plot_surface(
            xarray, yarray, zarray_a[:, :, frame_number], cmap="afmhot_r")
        plot[1] = ax.plot_surface(
            xarray, yarray, zarray_b[:, :, frame_number], cmap="Blues")
        # print(zarray[:, :, frame_number].shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("A (Red) vs. B (Blue)")

    a_surface = ax.plot_surface(
        xarray, yarray, zarray_a[:, :, 0], color='0.75', rstride=1, cstride=1)
    b_surface = ax.plot_surface(
        xarray, yarray, zarray_b[:, :, 0], color='0.75', rstride=1, cstride=1)
    plot = [a_surface, b_surface]

    # ax.set_zlim(0, 1.1)
    ani = animation.FuncAnimation(fig, change_plot, T_steps, fargs=(
        zarray_a, zarray_b, plot), interval=interval)

    plt.show()


def main():
    col = 100
    row = 100
    mat = np.full((row, col), -np.inf)
    n_map = mat.copy()
    n_map[0, 0] = 1
    n_map[row-1, col-1] = 0
    bounds = get_bounds(n_map)
    n_map = interp_n_matrix(n_map)
    # print(n_map)
    #n_map = uniform_random(n_map)

    l = .994
    m_map = mat.copy()
    m_map[0, 0] = 0
    m_map[row-1, col-1] = l
    m_map = interp_m_matrix(m_map)
    r = 8
    # print(m_map)
    #m_map = uniform_random(m_map)

    solver = ContinuousGraphSolver(n_map=n_map,
                                   m_map=m_map,
                                   time_steps=100,
                                   move_radius=r,
                                   boundary_coords=bounds
                                   )

    solver.solve(debug=False)

    x_dim = solver.bounds[1][0] - solver.bounds[0][0] + 1
    y_dim = solver.bounds[1][1] - solver.bounds[0][1] + 1
    a = solver.a
    b = solver.b
    T_steps = solver.time_steps

    plot(x_dim, y_dim, a, b, T_steps)


main()
