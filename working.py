import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#   Constants
G = 6.67430e-11 # Gravitational constant
AU = 1.496e11  # 1 Astronomical Unit in meters
YEAR = 3.154e7 # seconds

#   Initial conditions
TIME_MAX = 24*YEAR
TIME_STEP = 12000
# Masses
MASS_S = 2.99e30
MASS_A = 27.9e24
MASS_B = 2.35e28
# Radii
RAD_S = 9e8
RAD_A = 5e6
RAD_B = 4.5e7
# Positions
P_S = np.array([ 0.0 , 0.0 ])
P_A = np.array([ 5*AU , 0.0 ])
P_B = np.array([ -AU , AU*.7 ])
# Velocities
V_S = np.array([ 0.0 , 0.0 ])
V_A = np.array([ 0.0 , -16.8e3 ])
V_B = np.array([ 0.0 , -39.5e3 ])

initial_state = [P_S, P_A, P_B, V_S, V_A, V_B]

def three_body_equations(t, state, G, m1, m2, m3):
    # Unpack state vector
    p1, p2, p3, v1, v2, v3 = state
    r12 = np.linalg.norm(p1-p2)
    r23 = np.linalg.norm(p2-p3)
    r31 = np.linalg.norm(p3-p1)

    # Collision check
    if r12 < RAD_S or r12 < RAD_A:
        print("collision")
    if r23 < RAD_A or r23 < RAD_B:
        print("collision")
    if r31 < RAD_B or r31 < RAD_S:
        print("collision")

    # Accelerations
    a1 = -G * m2 * (p1-p2) / r12**3 -G * m3 * (p1-p3) / r31**3
    a2 = -G * m3 * (p2-p1) / r12**3 -G * m1 * (p2-p3) / r23**3
    a3 = -G * m1 * (p3-p1) / r31**3 -G * m2 * (p3-p2) / r23**3
    # Velocities
    v1 += a1 * TIME_STEP
    v2 += a2 * TIME_STEP
    v3 += a3 * TIME_STEP
    # Positions
    p1 += v1 * TIME_STEP
    p2 += v2 * TIME_STEP
    p3 += v3 * TIME_STEP
    # Return new state
    return [p1, p2, p3, v1, v2, v3]

# Intagration
t = 0
state = initial_state
x1_sol = []
y1_sol = []
x2_sol = []
y2_sol = []
x3_sol = []
y3_sol = []
while t < TIME_MAX:
    x1_sol.append(state[0][0])
    y1_sol.append(state[0][1])
    x2_sol.append(state[1][0])
    y2_sol.append(state[1][1])
    x3_sol.append(state[2][0])
    y3_sol.append(state[2][1])
    state = three_body_equations(TIME_STEP, state, G, MASS_S, MASS_A, MASS_B)
    t+=TIME_STEP

# Extract solution
plt.figure(figsize=(8,8))
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Three-Body Problem: S-A-B')
plt.grid(True)
plt.axis('equal')
# Plot trajectories
plt.plot(x1_sol, y1_sol, 'y', label='S')
plt.plot(x2_sol, y2_sol, 'b', label='A')
plt.plot(x3_sol, y3_sol, 'r', label='B')
# Initial Positions as larger circles
plt.scatter(x1_sol[0], y1_sol[0], color='y', marker='o')
plt.scatter(x2_sol[0], y2_sol[0], color='b', marker='o')
plt.scatter(x3_sol[0], y3_sol[0], color='r', marker='o')
plt.legend()
plt.show()