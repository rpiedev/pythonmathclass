import numpy as np
# 3 body sim for class instruction

class Body:
    def __init__(self, x, y, z, vx, vy, vz, mass, diameter):
        # kilometers
        self.x = x
        self.y = y
        self.z = z
        self.diameter = diameter
        # kilometers per second
        self.vx = vx
        self.vy = vy
        self.vz = vz

        # kilograms?
        self.mass = mass

# system constants
TimeStep = 0.001 #years
TimeMaximum = 1000 #years
GravConstant = 1

# system variables
timeElapsed = 0 #years

# Body variables and initial conditions
#             position | velocity
planetA = Body(0, 1, 1 , 0, 0, 0, 10, 10)
planetB = Body(1, 0, 1 , 0, 0, 0, 10, 10)
star    = Body(1, 1, 0 , 0, 0, 0, 10, 10)

# Functions
def calculateGravitationalEffects():
    # effects on planet A
    calculatedForce = (0, 0)
    # effects on planet B
    
    # effects on the Star

while timeElapsed <= TimeMaximum:
    calculateGravitationalEffects()
    timeElapsed += TimeStep