from ursina import *
import numpy as np

app = Ursina()

# Constants
G = 6.67430e-11  # gravitational constant
dt = 60 * 60     # time step: 1 hour

# Body class
class CelestialBody(Entity):
    def __init__(self, mass, position, velocity, color, radius):
        super().__init__(
            model='sphere',
            color=color,
            scale=radius,
            position=position,
        )
        self.mass = mass
        self.velocity = velocity
        self.trail = []

    def update_position(self, acceleration):
        # Velocity Verlet or simple Euler
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.trail.append(Vec3(self.position))
        if len(self.trail) > 300:
            self.trail.pop(0)

    def draw_trail(self):
        if len(self.trail) > 2:
            for i in range(len(self.trail) - 1):
                segment = Entity(
                    model=Mesh(vertices=[self.trail[i], self.trail[i+1]], mode='line'),
                    color=self.color,
                    scale=1,
                    add_to_scene_entities=False,
                )

# Initialize bodies: Sun, Earth, Moon
sun = CelestialBody(
    mass=1.989e30,
    position=Vec3(0, 0, 0),
    velocity=Vec3(0, 0, 0),
    color=color.yellow,
    radius=2
)

earth = CelestialBody(
    mass=5.972e24,
    position=Vec3(150e9, 0, 0),
    velocity=Vec3(0, 29780, 0),
    color=color.blue,
    radius=1
)

moon = CelestialBody(
    mass=7.348e22,
    position=Vec3(150e9 + 384.4e6, 0, 0),
    velocity=Vec3(0, 29780 + 1022, 0),
    color=color.white,
    radius=0.5
)

bodies = [sun, earth, moon]

def compute_accelerations():
    accelerations = [Vec3(0, 0, 0) for _ in bodies]
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i != j:
                r = bodies[j].position - bodies[i].position
                dist = max(r.length(), 1e7)  # prevent div by zero
                force_dir = r.normalized()
                a = G * bodies[j].mass / dist**2
                accelerations[i] += force_dir * a
    return accelerations

def update():
    accelerations = compute_accelerations()
    for i, body in enumerate(bodies):
        body.update_position(accelerations[i])
        body.draw_trail()

Sky()
EditorCamera()

app.run()
