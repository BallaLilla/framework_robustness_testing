import math
import numpy as np
import matplotlib.pyplot as plt

def transition_curve_parameters(start_angle, end_angle, length):
    # Convert angles to radians
    theta1 = math.radians(start_angle)
    theta2 = math.radians(end_angle)

    # Calculate the constant K, which depends on the difference in angles and length
    K = (theta2 - theta1) / (length * 2)

    # Calculate the radius at the beginning (R1) and the radius at the end (R2)
    R1 = 1 / K
    R2 = 1 / (K + (length / 2))

    return R1, R2, K, theta1, theta2

# Input values
start_angle = 0  # Start angle in degrees
end_angle = 10    # End angle in degrees
length = 5     # Length of the transition curve

# Calculate transition curve parameters
R1, R2, K, theta1, theta2 = transition_curve_parameters(start_angle, end_angle, length)

# Create points along the transition curve
t = np.linspace(0, length, 100)  # 100 points along the curve
theta = theta1 + K * t ** 2

# Calculate radii of curvature at each point
R = 1 / K + t

# Convert polar coordinates to Cartesian coordinates
x = R * np.cos(theta)
y = R * np.sin(theta)

# Plot the transition curve
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Transition Curve')
plt.axis('equal')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Transition Curve')
plt.grid(True)
plt.legend()
plt.show()
