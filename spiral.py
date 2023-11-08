import math
import matplotlib.pyplot as plt

def generate_spiral(start_angle, end_angle, x_start, y_start, length, num_points):
    points = []
    angle_increment = (end_angle - start_angle) / (num_points - 1)

    for i in range(num_points):
        angle = math.radians(start_angle + i * angle_increment)
        radius = i * (length / (num_points - 1))
        x_i = x_start + radius * math.cos(angle)
        y_i = y_start + radius * math.sin(angle)
        points.append((x_i, y_i))

    return points

start_angle = 360  # Kezdő szög (fokban)
end_angle = 0  # Végszög (fokban)
x_start, y_start = 0, 0  # Kezdeti pozíció
length = 10  # Spirál hossza
num_points = 10  # Pontok száma

points = generate_spiral(start_angle, end_angle, x_start, y_start, length, num_points)

x_values, y_values = zip(*points)

plt.plot(x_values, y_values, marker='o')
plt.title("Spirál szakasz")
plt.xlabel("X tengely")
plt.ylabel("Y tengely")
plt.grid(True)
plt.axis('equal')  # Az egyenlő arányú tengelyekhez
plt.show()
