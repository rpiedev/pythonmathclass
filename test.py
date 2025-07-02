from ursina import *
import numpy as np
# 3 body sim for class instruction

# Ursina 
sim = Ursina()
camera.position = (0,0,-10)

# Main Class
class Body:
    def __init__(self, position, velocity, mass, diameter, color):
        # 1 AU
        self.pos = position
        self.diameter = diameter
        # 1 AU per second
        self.vel = velocity

        # kilograms
        self.mass = mass

        self.sphere = Entity(model='sphere',texture='grass',color=color)
        self.sphere.scale = diameter
        self.sphere.position = position
        self.sphere.update = self.UpdatePos
    def UpdatePos(self):
        # Calculate force being exerted on this body from every other
        if self not in solarSystem:
            return
        totalForce = [0,0,0]
        for body in solarSystem:
            if body is not self:
                totalForce = np.add(totalForce, calculateForceGravity(self, body))
        #Calculate change to velocity (acceleration) based on force and mass
        self.vel[0] += totalForce[0] / self.mass * time.dt * TimeStep
        self.vel[1] += totalForce[1] / self.mass * time.dt * TimeStep
        #update position based on velocity
        self.pos[0] += self.vel[0] * time.dt * TimeStep
        self.pos[1] += self.vel[1] * time.dt * TimeStep
        self.sphere.position = self.pos
        

# system constants
TimeMaximum = 3000 
TimeStep = 100 # day
GravConstant = 2.407e-39 # Au^3/kg*s^2

# system variables
timeElapsed = 0 #years, actually seconds

# Body variables and initial conditions
#               position | velocity| m | d, color
#       Diameters are not accurate and for visibility in the simulation only

#Our sun is at the center of our system, has a mass of 1.989e30 kg, and a diameter of about 1.4e6 km
star    = Body([0, 0, 0],[0, 0, 0], 1.989e30, .5, color.red)

#The Earth is about 1 AU from the sun, has a mass of 5.972e24 kg, and a diameter of about 13e3 km
#Orbital velocity of about 6e6 km/s
planetA = Body([1, 0, 0],[0, .002, 0], 5.972e24, .3, color.yellow)
#planetB = Body([0, 0, 0],[0, -20, 0], 1e3, 5, color.green)

solarSystem = [star, planetA]

def calculateForceGravity(body1, body2):
    #calculate the radius betweent the bodies, this one is not square rooted yet
    distanceX = body1.pos[0] - body2.pos[0]
    distanceY = body1.pos[1] - body2.pos[1]
    distanceSquared = distanceX**2 + distanceY**2

    #angle = math.atan2(body1.pos[1] - body2.pos[1], body1.pos[0] - body2.pos[0])
    #forceCo = GravConstant * body1.mass * body2.mass / distanceSquared
    #return [-forceCo*math.cos(angle),-forceCo*math.sin(angle),0]

    distance = math.sqrt(distanceSquared)
    forceCo = GravConstant * body1.mass * body2.mass / distanceSquared
    return [ -forceCo*distanceX/distance, -forceCo*distanceY/distance, 0 ]
Entity()
sim.run()