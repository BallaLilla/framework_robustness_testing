import math
import matplotlib.pyplot as plt

def generate_euler_spiral(start_angle, end_angle, x_start, y_start, A, num_points):
    points = []
    angle_increment = (end_angle - start_angle) / (num_points - 1)

    for i in range(num_points):
        angle = math.radians(start_angle + i * angle_increment)
        theta = angle / A
        x_i = x_start + A * theta * math.cos(theta)
        y_i = y_start + A * theta * math.sin(theta)
        points.append((x_i, y_i))

    return points

start_angle = 0  # Kezdő szög (fokban)
end_angle = 6 * math.pi  # Végszög (radiánban)
x_start, y_start = 0, 0  # Kezdeti pozíció
A = 0.1  # Euler-spirál paramétere
num_points = 100  # Pontok száma

points = generate_euler_spiral(start_angle, end_angle, x_start, y_start, A, num_points)

x_values, y_values = zip(*points)

plt.plot(x_values, y_values, marker='o')
plt.title("Euler-spirál")
plt.xlabel("X tengely")
plt.ylabel("Y tengely")
plt.grid(True)
plt.axis('equal')  # Az egyenlő arányú tengelyekhez
plt.show()
