import math
import matplotlib.pyplot as plt

def generate_line(x, y, heading, length, num_points):
    points = []

    for i in range(num_points):
        x_i = x + (i / (num_points - 1)) * length * math.cos(math.radians(heading))
        y_i = y + (i / (num_points - 1)) * length * math.sin(math.radians(heading))
        points.append((x_i, y_i))

    return points

x_start, y_start = 0, 0
heading = 45
length = 10
num_points = 10

points = generate_line(x_start, y_start, heading, length, num_points)

x_values, y_values = zip(*points)

plt.plot(x_values, y_values, marker='o')
plt.title("10 pontból álló egyenes szakasz")
plt.xlabel("X tengely")
plt.ylabel("Y tengely")
plt.grid(True)
plt.show()
