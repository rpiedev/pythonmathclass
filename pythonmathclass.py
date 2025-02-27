from ursina import *

game = Ursina()

cube = Entity(model='cube', color = rgb(10,90,10), scale = 2, collider='box')

def spin():
    cube.animate('rotation_y', cube.rotation_y+360, duration=2, curve=curve.in_out_expo)

cube.on_click = spin

EditorCamera()

game.run()