import numpy as np
import matplotlib.pyplot as plt

def generate_arc_segment(x, y, h, radius, angle, num_points):
    # Az ív középpontjának számítása
    if angle > 0:
        center_hdg = h - np.pi / 2
    else:
        center_hdg = h + np.pi / 2

    center_x = x - np.cos(center_hdg) * radius
    center_y = y - np.sin(center_hdg) * radius

    # Az ív koordinátáinak számítása
    arc_points = []
    
    for i in range(num_points + 1):
        theta = h + (i / num_points) * angle
        point_x = center_x + radius * np.cos(theta)
        point_y = center_y + radius * np.sin(theta)
        arc_points.append((point_x, point_y))

    return arc_points

# Példa használatra egy 45 fokos ív generálásához 20 mintaponttal
x_start = 0.0
y_start = 0.0
heading = np.pi / 4  # Kezdeti irány radiánban (45 fok)
arc_radius = 10.0
arc_angle = np.pi / 2  # Az ív 45 fokos
num_points = 20  # Pontok száma

arc_segment = generate_arc_segment(x_start, y_start, heading, arc_radius, arc_angle, num_points)

# Az ív kirajzolása
arc_points = np.array(arc_segment)
plt.plot(arc_points[:, 0], arc_points[:, 1], marker='o')
plt.axis('equal')
plt.title('45 fokos ív')
plt.grid(True)
plt.show()

