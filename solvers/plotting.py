import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# N = 50
# fps = 250
# T_steps = 75

# x = np.linspace(-4, 4, N + 1)
# xarray, yarray = np.meshgrid(x, x)
# # print(xarray.shape, yarray.shape)
# zarray = np.zeros((N + 1, N + 1, T_steps))

# f = lambda x, y, sig: 1 / np.sqrt(sig) * np.exp(-(x ** 2 + y ** 2) / sig ** 2)

# for i in range(T_steps):
#     zarray[:, :, i] = f(xarray, yarray, 1.5 + np.sin(i * 2 * np.pi / T_steps))

fps = 250
T_steps = 50

x_dim, y_dim = (10, 10)

f = lambda x, y, sig: 1 / np.sqrt(sig) * np.exp(-((x-x_dim/2) ** 2 + (y-y_dim/2) ** 2) / sig ** 2)

x = np.arange(x_dim)
y = np.arange(y_dim)
xarray, yarray = np.meshgrid(x,y)
zarray = np.zeros((x_dim, y_dim, T_steps))
for i in range(T_steps):
    zarray[:, :, i] = f(xarray, yarray, 1.5 + np.sin(i * 2 * np.pi / T_steps))
    # zarray[:, :, i] = np.ones((x_dim, y_dim)) * i

def change_plot(frame_number, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(xarray, yarray, zarray[:, :, frame_number], cmap="afmhot_r")
    # print(zarray[:, :, frame_number].shape)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plot = [ax.plot_surface(xarray, yarray, zarray[:, :, 0], color='0.75', rstride=1, cstride=1)]

# ax.set_zlim(0, 1.1)
ani = animation.FuncAnimation(fig, change_plot, T_steps, fargs=(zarray, plot), interval=1000 / fps)

plt.show()