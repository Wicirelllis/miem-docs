from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(dpi=150)
ax = fig.add_subplot(111, projection='3d')

d = Poly3DCollection(
    [
        [[-1, 6, 0], [10, 6, 0], [10, 10, 0], [3, 10, 0], [3, 22, 0], [-1, 22, 0]],
        [[3, 10, 0.25], [6, 10, 0.25], [6, 14, 0.25], [3, 14, 0.25]],
        [[6, 10, 0.35], [10, 10, 0.35], [10, 14, 0.35], [6, 14, 0.35]],
        [[3, 14, 0.4], [6, 14, 0.4], [6, 18, 0.4], [3, 18, 0.4]],
        [[6, 14, 0.55], [10, 14, 0.55], [10, 18, 0.55], [6, 18, 0.55]],
        [[3, 18, 0.87], [6, 18, 0.87], [6, 22, 0.87], [3, 22, 0.87]],
        [[6, 18, 1], [10, 18, 1], [10, 22, 1], [6, 22, 1]],
    ],
    facecolors=cm.get_cmap("YlOrRd")((0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8))
)
ax.add_collection3d(d)

vl_x = [[3, 3], [6, 6], [10, 10], [3, 3], [6, 6], [10, 10], [3, 3], [6, 6], [10, 10], [3, 3], [6, 6]]
vl_y = [[10, 10], [10, 10], [10, 10], [14, 14], [14, 14], [14, 14], [18, 18], [18, 18], [18, 18], [22, 22], [22, 22]]
vl_z = [[0, 0.25], [0, 0.35], [0, 0.35], [0, 0.4], [0.25, 0.55], [0.35, 0.55], [0, 0.87], [0.4, 1], [0.55, 1], [0, 0.87], [0.87, 1]]
for i in range(11):
    ax.plot(vl_x[i], vl_y[i], vl_z[i], linewidth=1.5, color="k")

ax.set_xlim([-1,10])
ax.set_ylim([6,22])
ax.set_zlim([0,1])

ax.set_box_aspect((11, 16, 10))
ax.view_init(elev=30, azim=-140)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Функция распределения")

plt.savefig("hw_6.png")
plt.show()
