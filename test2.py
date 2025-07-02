from ursina import *
import numpy as np
# 3 body sim for class instruction

# Ursina 
sim = Ursina()
camera.position = (0,0,-10)

# Units are kilometers, kilograms, and seconds

class Body:
    def __init__(self, position, velocity, mass, diameter, color):
        self.p = position
        self.v = velocity
        self.m = mass

        self.entity = Entity(model='sphere',texture='grass',color=color)
        self.entity.scale = diameter
        self.entity.position = self.p

class OrbitalSystem:
    def __init__(self, G):
        self.gravitationalConstant = G
        self.bodyList = []
    def addBody(self, position, velocity, mass, diameter, color):
        #               Vec3  ,   Vec3,  float,   float ,  rgb
        newBody = Body(position, velocity, mass, diameter, color)
        self.bodyList.append(newBody)
    def timeStep(self):
        firstBody = self.bodyList[0]
        for body in self.bodyList:
            if body is firstBody:
                continue
            distance = Vec3( firstBody.p.x-body.p.x, firstBody.p.y-body.p.y, firstBody.p.z-body.p.z )
            radiusSquared = (distance[0]**2+distance[1]**2+distance[2]**2)
            forceScalar = -self.gravitationalConstant * firstBody.m * body.m / radiusSquared


solarSystem = OrbitalSystem(6.674e-11)
solarSystem.addBody(Vec3(0,0,0),Vec3(0,0,0),1,1,color.red)
solarSystem.addBody(Vec3(3,0,0),Vec3(0,0,0),1,1,color.green)

while True:
