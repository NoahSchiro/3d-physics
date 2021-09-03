from classes import *
import math

# Constant variables
scene.width  = 1600
scene.height = 800

# Create field
my_field = electric_field()
my_charge = point_charge(0.001, -1E-9, 10, 10, 10)

while True:
    rate(20)

    if my_charge.pos[0] >= 10:
        my_charge.apply_force([-0.1, -0.1, -0.1])
    if my_charge.pos[0] <= -10:
        my_charge.apply_force([0.1, 0.1, 0.1])

    my_field.point_to_charge(my_charge)
    my_field.change_magnitude(my_charge)
    my_charge.update_position()